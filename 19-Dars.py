import os, json, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "8937424864:AAEVuSxbNEg8Q614Kx3Si0MBlNyYa_J3sco"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DISHES_FILE, CATEGORIES_FILE, USERS_FILE = "dishes.json", "categories.json", "users.json"

# --- JSON FAYLLAR BILAN ISHLASH ---
def load_json(file_name, default):
    try:
        with open(file_name, "r", encoding="utf-8") as f: 
            return json.load(f)
    except FileNotFoundError: 
        return default

def save_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False, indent=2)

DISHES = load_json(DISHES_FILE, [])
CATEGORIES = load_json(CATEGORIES_FILE, ["breakfast", "lunch", "dinner", "dessert"])
USERS = load_json(USERS_FILE, {})

def get_lang(user_id):
    return USERS.get(str(user_id), "en")

# --- TARJIMAlAR LUG'ATI ---
TRANSLATIONS = {
    "welcome": {
        "en": "Hello! I'm the Dinner Picker bot. Use /language to change language.",
        "ru": "Привет! Я бот Dinner Picker. Используйте /language для смены языка.",
        "uz": "Salom! Men Dinner Picker botiman. Tilni o'zgartirish uchun /language komandasidan foydalaning."
    },
    "ask_dish_name": {
        "en": "Enter dish name:", "ru": "Введите название блюда:", "uz": "Taom nomini kiriting:"
    },
    "ask_dish_photo": {
        "en": "Send dish photo:", "ru": "Отправьте фото блюда:", "uz": "Taom rasmini yuboring:"
    },
    "ask_dish_category": {
        "en": "Select category:", "ru": "Выберите категорию:", "uz": "Kategoriyani tanlang:"
    },
    "dish_added": {
        "en": "Saved! Dish: {name}", "ru": "Сохранено! Блюдо: {name}", "uz": "Saqlandi! Taom: {name}"
    },
    "ask_cat_name": {
        "en": "Enter new category name:", "ru": "Введите название новой категории:", "uz": "Yangi kategoriya nomini kiriting:"
    },
    "cat_exists": {
        "en": "Category '{name}' already exists.", "ru": "Категория '{name}' уже существует.", "uz": "'{name}' kategoriyasi allaqachon bor."
    },
    "cat_added": {
        "en": "Added category: {name}", "ru": "Добавлена категория: {name}", "uz": "Kategoriya qo'shildi: {name}"
    },
    "cat_usage": {
        "en": "Usage: /removecategory <name>", "ru": "Использование: /removecategory <название>", "uz": "Foydalanish: /removecategory <nomi>"
    },
    "cat_not_found": {
        "en": "Category '{name}' not found.", "ru": "Категория '{name}' не найдена.", "uz": "'{name}' kategoriyasi topilmadi."
    },
    "cat_in_use": {
        "en": "Can't remove! Some dishes use this category.", "ru": "Нельзя удалить! Эта категория используется в блюдах.", "uz": "O'chirib bo'lmaydi! Ichida taomlar bor."
    },
    "cat_removed": {
        "en": "Removed category: {name}", "ru": "Удалена категория: {name}", "uz": "Kategoriya o'chirildi: {name}"
    },
    "empty_dishes": {
        "en": "No dishes added yet. Use /add first.", "ru": "Блюд пока нет. Сначала используйте /add.", "uz": "Hozircha taomlar yo'q. Avval /add yordamida qo'shing."
    },
    "no_dishes_in_cat": {
        "en": "No dishes in this category.", "ru": "В этой категории нет блюд.", "uz": "Bu kategoriyada taom yo'q."
    },
    "random_pick": {
        "en": "Choice: {name}", "ru": "Выбор: {name}", "uz": "Tanlov: {name}"
    }
}

def t(key, lang, **kwargs):
    return TRANSLATIONS[key][lang].format(**kwargs)

# --- FSM VA TUGMALAR ---
class AddDish(StatesGroup):
    waiting_for_name, waiting_for_photo, waiting_for_category = State(), State(), State()

class AddCategory(StatesGroup):
    waiting_for_name = State()

def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="English 🇬🇧", callback_data="lang:en")
    builder.button(text="Русский 🇷🇺", callback_data="lang:ru")