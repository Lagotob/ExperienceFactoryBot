from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

router = Router()

# -----

async def get_product(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None

            data = await resp.json()
            return data

# -----

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello World: /product ID \n\n")


@router.message(Command("product"))
async def print_product(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer("Xato! Please enter a /product ID")
        return

    product_id = parts[1]

    if not product_id.isdigit():
        await message.answer("Xato! Please enter a /product ID(son)")
        return

    await message.answer("Searching ...")

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer("Uxshamadi!")
        return

    if product is None:
        await message.answer("Topilmadi!")
        return

    title = product.get("title", "Nomsiz")
    price = product.get("price", "Tekin")
    desc = product.get("description", "Prosta")
    category = product.get("category", "Prosta")

    text = (
        f"<b>{title}</b>\n\n"
        f"Katigoriya: <i>{category}</i>\n"
        f"Narx: <b>{price}</b>\n"
        f"{desc}"
    )

    await message.answer(text, parse_mode="HTML")
