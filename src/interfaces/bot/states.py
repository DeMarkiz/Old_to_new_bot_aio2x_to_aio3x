from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    """Состояния для формы пользователя."""
    name = State()
    info = State()
    photo = State()


class UserFormData:
    """Данные формы пользователя."""
    
    def __init__(self):
        self.name: str = ""
        self.info: str = ""
        self.photo: str = ""


class UserStates(StatesGroup):
    """Состояния пользователя"""
    waiting_for_name = State()
    waiting_for_photo = State()
    waiting_for_info = State() 