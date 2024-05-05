from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    id_u = State()
    username = State()
    name = State()
    age = State()
    clas = State()
    gender = State()
    about = State()
    photo = State()

class Assessment(StatesGroup):
    id_user = State()
    id_other = State()
    asses = State()
