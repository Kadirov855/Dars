import os
import json
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Bot tokeningizni yozing
BOT_TOKEN = "BU_YERGA_TOKENINGIZNI_YOZING"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ma'lumotlarni fayldan yuklab olish funksiyasi
def load_dishes():
    if os.path.exists("dishes.json"):
        with open("dishes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Ma'lumotlarni faylga saqlash funksiyasi
def save_dishes(data):
    with open("dishes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Taomlar ro'yxatini yuklaymiz
DISHES = load_dishes()


# --- FSM (Holatlar) ---
class AddDish(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()


# --- Buyruqlar (Handlers) ---

# /start buyrug'i
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Salom! Men taomlar botiman.\n"
        "Buyruqlar:\n"
        "/add - Yangi taom qo'shish\n"
        "/list - Taomlar ro'yxati\n"
        "/random - Tasodifiy taom tanlash\n"
        "/photo <raqam> - Taom rasmini ko'rish"
    )

# /add buyrug'i (1-bosqich: Nomini so'rash)
@dp.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await message.answer("Qanday taom qo'shmoqchisiz? Nomini kiriting:")
    await state.set_state(AddDish.waiting_for_name)

# Taom nomini qabul qilish (2-bosqich: Rasm so'rash)
@dp.message(AddDish.waiting_for_name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Endi ushbu taomning rasmini yuboring.\nAgarda rasm bo'lmasa, /skip buyrug'ini bosing.")
    await state.set_state(AddDish.waiting_for_photo)

# Rasm yuborilganda ishlaydigan qism
@dp.message(AddDish.waiting_for_photo, F.photo)
async def process_dish_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = message.photo[-1].file_id  # Eng sifatli rasm ID-sini olish

    DISHES.append({"name": data["name"], "photo": file_id})
    save_dishes(DISHES)

    await state.clear()
    await message.answer(f"Muvaffaqiyatli qo'shildi: {data['name']} (rasmi bilan) ✅")

# Rasm tashlab ketilganda (/skip) ishlaydigan qism
@dp.message(AddDish.waiting_for_photo, Command("skip"))
async def process_dish_no_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()

    DISHES.append({"name": data["name"], "photo": None})
    save_dishes(DISHES)

    await state.clear()
    await message.answer(f"Muvaffaqiyatli qo'shildi: {data['name']} (rasmsiz) 🍽️")

# /list buyrug'i (Ro'yxatni ko'rsatish)
@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    if not DISHES:
        await message.answer("Taomlar ro'yxati bo'sh. Avval taom qo'shing: /add")
        return

    text = "Sizning taomlaringiz ro'yxati:\n"
    for i, dish in enumerate(DISHES, start=1):
        # Taomning rasmi bor-yo'qligiga qarab belgi qo'yamiz (Kutilmagan xatoni oldini olish uchun .get() ishlatildi)
        marker = "📷" if dish.get("photo") else "❌"
        text += f"{i}. {dish['name']} {marker}\n"

    await message.answer(text)

# /random buyrug'i (Tasodifiy taom tanlash)
@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    if not DISHES:
        await message.answer("Ro'yxat bo'sh. Avval taom qo'shing.")
        return

    dish = random.choice(DISHES)

    if dish.get("photo"):
        await message.answer_photo(dish["photo"], caption=f"Bugun buni yeb ko'ring: {dish['name']} 🍽️")
    else:
        await message.answer(f"Bugun buni yeb ko'ring: {dish['name']} 🍽️")

# BONUS VAZIFA: /photo <raqam> buyrug'i
@dp.message(Command("photo"))
async def cmd_photo(message: types.Message):
    # Buyruq yonidan yozilgan matnni olish (masalan: /photo 2 -> "2")
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Iltimos buyruqni to'g'ri kiriting. Masalan: `/photo 1`")
        return

    index = int(args[1]) - 1  # Foydalanuvchi 1 deganda koddagi 0-indeks nazarda tutiladi

    if index < 0 or index >= len(DISHES):
        await message.answer("Bunday raqamli taom topilmadi.")
        return

    dish = DISHES[index]

    if dish.get("photo"):
        await message.answer_photo(dish["photo"], caption=f"{dish['name']} taomining rasmi")
    else:
        await message.answer(f"Afsuski, '{dish['name']}' taomiga rasm biriktirilmagan.")


# Botni ishga tushirish
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))