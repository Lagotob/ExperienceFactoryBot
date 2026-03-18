from aiogram import Router, F
from aiogram.filters import  Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Boshlash")],
            [KeyboardButton(text="Ma\'lumot"),KeyboardButton(text="Yordam")]
        ],
        resize_keyboard=True
    )

    return keyboard

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Sayt", url="https://google.com")],
            [InlineKeyboardButton(text="Batafsil", callback_data="batafsil")],
        ]
    )

    return keyboard


@router.callback_query(lambda query: query.data == "batafsil")
async def more_info(callback: CallbackQuery):
    await callback.message.answer("Bla Bla Bla \n"
                                  "Bla bla bla")
    await callback.answer()


@router.message(Command("start"))
@router.message(F.text.lower() == "boshlash")
async def start(message: Message):
    await message.answer(f"*Salom* {message.from_user.first_name}! \n"
                         f"/help ni _yoz_",
                         parse_mode="Markdown")

@router.message(Command("help"))
@router.message(F.text.lower() == "yordam")
async def commands(message: Message):
    await message.answer("Buyruqlar: "
                         "\n /start - <b>Start</b> "
                         "\n /help - <i>Yordam</i> "
                         "\n /about - <a href='google.com'>Biz haqimizda</a>",
                         parse_mode="HTML",
                         reply_markup=get_main_reply_keyboard())

@router.message(Command("about"))
@router.message(F.text.lower() == "ma\'lumot")
async def about(message: Message):
    await message.answer("ExperienceFactory🤩", reply_markup=get_main_inline_keyboard())

@router.message()
async def text(message: Message):
    await message.answer("NO, No, No")