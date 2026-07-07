import json

DISHES_FILE = "dishes.json"

def load_dishes():
    try:
        with open(DISHES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_dishes(dishes):
    with open(DISHES_FILE, "w") as file:
        json.dump(dishes, file, ensure_ascii=False, indent=2)

DISHES = load_dishes()

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class AddDish(StatesGroup):
    waiting_for_name = State()
