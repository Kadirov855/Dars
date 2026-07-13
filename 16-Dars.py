import json
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Bot tokeningizni yozing
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# JSON fayl bilan ishlash funksiyalari
def load_dishes():
    try:
        with open("dishes.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_dishes(dishes):
    with open("dishes.json", "w") as f:
        json.dump(dishes, f, indent=4)

# Bot ishga tushganda ma'lumotlarni yuklaymiz
DISHES = load_dishes()

# 1. FSM uchun holatlar (States)
class AddDish(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Taomlar botiga xush kelibsiz.\nKomandalar: /add, /list, /random")

# 2. Taom qo'shishni boshlash (/add)
@dp.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await message.answer("Qanday taom qo'shmoqchisiz?")
    await state.set_state(AddDish.waiting_for_name)

# Taom nomini qabul qilish
@dp.message(AddDish.waiting_for_name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Endi ushbu taomning rasmini yuboring.\nAgar rasm bo'lmasa, /skip buyrug'ini yozing.")
    await state.set_state(AddDish.waiting_for_photo)

# Taom rasmini qabul qilish (Rasm yuborilsa)
@dp.message(AddDish.waiting_for_photo, F.photo)
async def process_dish_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = message.photo[-1].file_id  # Eng sifatli rasm ID-sini olamiz

    DISHES.append({"name": data["name"], "photo": file_id})
    save_dishes(DISHES)

    await state.clear()
    await message.answer(f"Muvaffaqiyatli qo'shildi: {data['name']} (rasmi bilan) 📷")

# Rasmni o'tkazib yuborish (/skip bosilsa)
@dp.message(AddDish.waiting_for_photo, Command("skip"))
async def process_dish_no_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()

    DISHES.append({"name": data["name"], "photo": None})
    save_dishes(DISHES)

    await state.clear()
    await message.answer(f"Muvaffaqiyatli qo'shildi: {data['name']} (rasmsiz)")

# 3. Tasodifiy taom tanlash (/random)
@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    if not DISHES:
        await message.answer("Ro'yxat bo'sh! Avval taom qo'shing: /add")
        return

    dish = random.choice(DISHES)
    
    # .get() ishlatish eski ma'lumotlar o'chib ketganda xatolik bermasligi uchun kerak
    photo = dish.get("photo") 

    if photo:
        await message.answer_photo(photo, caption=f"Bugun nima yeymiz: {dish['name']}?")
    else:
        await message.answer(f"Bugun nima yeymiz: {dish['name']}? (Bu taomning rasmi yo'q)")

# 4. Taomlar ro'yxatini ko'rish (/list)
@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    if not DISHES:
        await message.answer("Taomlar ro'yxati bo'sh.")
        return

    text = "Mavjud taomlar ro'yxati:\n"
    for i, dish in enumerate(DISHES, start=1):
        # Agar rasm bo'lsa kamera belgisi qo'yiladi
        marker = "📷" if dish.get("photo") else "❌ (rasmsiz)"
        text += f"{i}. {dish['name']} - {marker}\n"

    await message.answer(text)

# Botni ishga tushirish
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))