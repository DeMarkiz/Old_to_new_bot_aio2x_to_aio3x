from aiogram import Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.application.use_cases.user_management import UserManagementUseCase
from src.application.use_cases.rating_management import RatingManagementUseCase
from src.domain.entities.user import User
from .filters import CreatorFilter, RegistrationFilter, NonRegistrationFilter
from .states import UserForm, UserFormData
from .errors import Errors
from src.application.services.user_service import UserService
from src.application.services.rating_service import RatingService
from src.interfaces.bot.states import UserStates
from src.interfaces.bot.filters import UserFilter
from src.interfaces.bot.dependencies import get_user_service, get_rating_service


def register_handlers(dp: Dispatcher) -> None:
    """Регистрация всех обработчиков команд"""
    router = Router()
    
    # Команды
    router.message.register(start_handler, Command(commands=["start"]))
    router.message.register(help_handler, Command(commands=["help"]))
    router.message.register(profile_handler, Command(commands=["profile"]))
    router.message.register(settings_handler, Command(commands=["settings"]))
    router.message.register(registration_handler, Command(commands=["register"]))
    
    # Обработчики состояний
    router.message.register(
        set_user_info_handler,
        StateFilter(UserStates.waiting_for_name),
        UserFilter()
    )
    router.message.register(
        set_photo_handler,
        StateFilter(UserStates.waiting_for_photo),
        UserFilter()
    )
    
    # Обработчики кнопок
    router.message.register(
        cancel_handler,
        F.text == "Отмена",
        UserFilter()
    )
    router.message.register(
        rating_handler,
        F.text == "Рейтинг",
        UserFilter()
    )
    router.message.register(
        press_handler,
        F.text == "Нажать",
        UserFilter()
    )
    router.message.register(
        settings_handler,
        F.text == "Настройки",
        UserFilter()
    )
    
    dp.include_router(router)


async def start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рейтинг"), KeyboardButton(text="Нажать")],
            [KeyboardButton(text="Настройки")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать! Я бот для подсчета нажатий.\n"
        "Используйте /help для получения списка команд.",
        reply_markup=keyboard
    )


async def help_handler(message: Message) -> None:
    """Обработчик команды /help."""
    await message.answer(
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/help - Показать справку\n"
        "Рейтинг - Показать рейтинг пользователей\n"
        "Нажать - Увеличить счетчик нажатий\n"
        "Настройки - Настроить профиль"
    )


async def profile_handler(message: Message, user_service: UserService) -> None:
    """Обработчик команды /profile."""
    user = await user_service.get_user(message.from_user.id)
    if not user:
        await message.answer("Вы не зарегистрированы. Используйте /register для регистрации.")
        return
        
    text = (
        f"👤 Ваш профиль:\n\n"
        f"Имя: {user.name}\n"
        f"Информация: {user.info}\n"
        f"Нажатий: {user.taps}\n"
    )
    
    if user.photo:
        await message.answer_photo(user.photo, caption=text)
    else:
        await message.answer(text)


async def settings_handler(message: Message, state: FSMContext) -> None:
    """Обработчик команды /settings."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True
    )
    await message.answer(
        "Введите ваше имя:",
        reply_markup=keyboard
    )
    await state.set_state(UserStates.waiting_for_name)


async def registration_handler(message: Message, state: FSMContext) -> None:
    """Обработчик команды /register."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать! Давайте зарегистрируем вас.\n"
        "Введите ваше имя:",
        reply_markup=keyboard
    )
    await state.set_state(UserStates.waiting_for_name)


async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Обработчик команды отмены."""
    await message.answer("Операция отменена.")
    if await state.get_state() is not None:
        await state.clear()


async def rating_handler(
    message: Message,
    user_management: UserManagementUseCase,
    rating_management: RatingManagementUseCase,
) -> None:
    """Обработчик команды рейтинга."""
    # Получаем пользователя
    user = await user_management.get_user_by_telegram_id(message.from_user.id)
    
    # Получаем топ пользователей
    top_users = await rating_management.get_top_users(limit=10)
    
    # Получаем общее количество нажатий
    total_taps = await rating_management.get_total_taps()
    
    # Формируем сообщение
    text = (
        f"📊 Рейтинг пользователей\n\n"
        f"Ваши нажатия: {user.taps}\n"
        f"Всего нажатий: {total_taps}\n\n"
        "Топ пользователей:\n"
    )
    
    for i, top_user in enumerate(top_users, 1):
        text += f"{i}. {top_user.username or 'Аноним'}: {top_user.taps}\n"
    
    await message.answer(text)


async def press_handler(
    message: Message,
    user_management: UserManagementUseCase,
    rating_management: RatingManagementUseCase,
) -> None:
    """Обработчик команды нажатия."""
    # Получаем пользователя
    user = await user_management.get_user_by_telegram_id(message.from_user.id)
    
    # Увеличиваем счетчик нажатий
    updated_user = await rating_management.increment_taps(user.id)
    
    await message.answer(f"Нажатий: {updated_user.taps}")


async def set_user_info_handler(message: Message, state: FSMContext) -> None:
    """Обработчик команды настройки профиля."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True
    )
    await message.answer(
        "Введите ваше имя:",
        reply_markup=keyboard
    )
    await state.set_state(UserForm.name)


async def set_name_handler(message: Message, state: FSMContext) -> None:
    """Обработчик ввода имени."""
    await state.update_data(name=message.text)
    await message.answer("Введите информацию о себе:")
    await state.set_state(UserForm.info)


async def set_info_handler(message: Message, state: FSMContext) -> None:
    """Обработчик ввода информации."""
    await state.update_data(info=message.text)
    await message.answer("Отправьте фотографию:")
    await state.set_state(UserForm.photo)


async def set_photo_handler(
    message: Message,
    state: FSMContext,
    user_management: UserManagementUseCase,
    rating_management: RatingManagementUseCase,
) -> None:
    """Обработчик отправки фотографии."""
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию.")
        return
    
    # Получаем данные формы
    form_data = await state.get_data()
    
    # Получаем пользователя
    user = await user_management.get_user_by_telegram_id(message.from_user.id)
    
    # Обновляем информацию о пользователе
    await user_management.update_user(
        user.id,
        first_name=form_data["name"],
    )
    await rating_management.update_user_info(user.id, form_data["info"])
    
    # Сохраняем фотографию
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    photo_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"
    await rating_management.update_user_photo(user.id, photo_url)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рейтинг"), KeyboardButton(text="Нажать")],
            [KeyboardButton(text="Настройки")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "Профиль успешно обновлен!",
        reply_markup=keyboard
    ) 
    await state.clear() 