from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from keyboards.reply_button import *
from aiogram import F

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.react([types.ReactionTypeEmoji(emoji='👍')])
    await message.answer(f"<b>Assalomu alaykum, <code>{message.from_user.full_name}</code>!</b>",reply_markup=reply_kb,parse_mode="html")

@router.message(F.text == "➕ So'rovnomada qatnashish")
async def handle_message(message: Message):
    await message.answer("<b>Kafedralardan birini tanlang!</b>",parse_mode="html",reply_markup=reply_kb_2)

@router.message(F.text.startswith("🏢"))
async def kofedra(message: Message):
    topic_name = message.text[2:].strip()
    reply_kb_3 = filter_teachers(topic_name)
    await message.answer("<b>Ustozni tanlang!</b>",reply_markup=reply_kb_3,parse_mode="html")

@router.message(F.text.startswith("👩‍🏫") | F.text.startswith("👨‍🏫"))
async def status(message: Message):
    await message.answer("cascascas")