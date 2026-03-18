from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import  Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from forms.user import Form
from aiogram.types import FSInputFile

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Registratsiyadan uting \n Ismingiz:")
    await state.set_state(Form.name)


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Uchirildi!")


@router.message(Form.name, F.text)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())

    await message.answer("Saqlandi! \nEndi yoshingiz:")
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Xatolik, Son kiriting!")
        return

    if int(message.text) < 1 or int(message.text) > 100:
        await message.answer("Xatolik, Tug\'ri yosh kiriting!")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Saqlandi! \nEndi Email:")
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
async def get_email(message: Message, state: FSMContext):
    email_text = message.text
    if "@" not in email_text or "." not in email_text:
        await message.answer("Xatolik, Email ni to\'liq kiriting!")
        return

    await state.update_data(email=email_text)

    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")

    await message.answer(f"Saqlandi! \n"
                         f"Ismingiz: {name}\n"
                         f"Yoshingiz: {age}\n"
                         f"Email: {email}")
    await state.clear()


@router.message(F.photo)
async def get_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(f"Rasm!\n"
                         f"IDsi: <code>{file_id}</code>",
                         parse_mode="HTML")

    await message.answer_photo(file_id, caption="Rasm!")


@router.message(F.video)
async def get_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(f"Video!\n"
                         f"IDsi: <code>{file_id}</code>\n"
                         f"Duration: <code>{duration}</code>",
                         parse_mode="HTML")

    await message.answer_video(file_id, caption="Video!")


@router.message(F.animation)
async def get_animation(message: Message):
    animation = message.animation

    await message.answer(f"Animatsiya!\n"
                         f"IDsi: <code>{animation.file_id}</code>",
                         parse_mode="HTML")

    await message.answer_animation(animation.file_id, caption="Video!")


@router.message(F.document)
async def get_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'documents/{document.file_name}'

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer(f"Document Saved!\n")


@router.message(Command("file"))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')

    await message.answer_document(file)
