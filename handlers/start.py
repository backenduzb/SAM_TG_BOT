from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from keyboards.reply_button import *
from aiogram import F
from utils.user_data import answered_questions
from utils.quest import queastions
from utils.teacher_id import get_teacher_id

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

    answered_questions[message.from_user.username] = str(message.text).replace("👩‍🏫","").replace("👨‍🏫","")

    answered_questions[str(message.from_user.id)] += 1

    await message.answer(queastions[answered_questions[str(message.from_user.id)]-1],reply_markup=reply_kb_3)


@router.message(F.text.in_(["Yaxshi", "Past", "O'rtacha", "Juda yaxshi", "Yomon"]))
async def its_user_answer(message:Message):

    text = message.text

    if answered_questions[str(message.from_user.id)] <= 7:


        if text == "Yaxshi":
            pass
        elif text == "Past":
            pass
        elif text == "O'rtacha":
            pass
        elif text == "Juda yaxshi":
            pass
        elif text == "Yomon":
            pass


        teacher_name = answered_questions[message.from_user.username].strip()
        teacher_id = get_teacher_id(teacher_name)
        
        if teacher_id:
            await message.answer(f"Ustoz id {teacher_id}")
        await message.answer(queastions[answered_questions[str(message.from_user.id)]-1],reply_markup=reply_kb_3)
        
