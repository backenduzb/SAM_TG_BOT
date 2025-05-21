from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from keyboards.reply_button import *
from aiogram import F
from utils.user_data import answered_questions, total_answer
from utils.quest import queastions
from utils.teacher_id import get_teacher_telegram_id, get_teacher_id
import requests
from data.config import url_edit_teacher
from data.bot import bot
from utils.teacher_data import get_teacher_status


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    
    global total_answer
    answered_questions[message.from_user.username] = ""
    answered_questions[str(message.from_user.id)] = 0
    answered_questions[f"{message.from_user.username}_kafedra"] = ""

    total_answer = "<b>📑 Sizning javoblaringiz.</b> \n\n"
    await message.react([types.ReactionTypeEmoji(emoji='👍')])
    await message.answer(f"<b>Assalomu alaykum, <code>{message.from_user.full_name}</code>!</b>",reply_markup=reply_kb,parse_mode="html")

@router.message(F.text == "➕ So'rovnomada qatnashish")
async def handle_message(message: Message):
    await message.answer("<b>Kafedralardan birini tanlang!</b>",parse_mode="html",reply_markup=reply_kb_2)

@router.message(F.text.startswith("🏢"))
async def kofedra(message: Message):
    global total_answer
    answered_questions[f"{message.from_user.username}_kafedra"] = str(message.text).replace("🏢","").strip()
    total_answer += f"<code>{answered_questions[f'{message.from_user.username}_kafedra']}</code> - kafedra.\n"
    topic_name = message.text[2:].strip()
    reply_kb_3 = filter_teachers(topic_name)
    await message.answer(" <b>Ustozni tanlang!</b>",reply_markup=reply_kb_3,parse_mode="html")

@router.message(F.text.startswith("👩‍🏫") | F.text.startswith("👨‍🏫"))
async def status(message: Message):

    global total_answer


    answered_questions[message.from_user.username] = str(message.text).replace("👩‍🏫","").replace("👨‍🏫","").strip()

    total_answer += f"<code>{answered_questions[message.from_user.username]}</code> - o'qituvchi. \n\n<pre>"

    answered_questions[str(message.from_user.id)] += 1

    await message.answer(f"<b>{queastions[answered_questions[str(message.from_user.id)]-1]}</b>",parse_mode="html",reply_markup=reply_kb_3)


@router.message(F.text.in_(["Yaxshi", "Past", "O'rtacha", "Juda yaxshi", "Yomon"]))
async def its_user_answer(message: Message):
    global total_answer

    text = message.text

    if answered_questions[str(message.from_user.id)] <= 6:

        await message.react([types.ReactionTypeEmoji(emoji='👌')])
        teacher_name = answered_questions[message.from_user.username].strip()
        teacher_id = get_teacher_id(answered_questions[message.from_user.username])

        edited_url = f"{url_edit_teacher}{teacher_id}/"
        print(edited_url)
        
        total_answer += f"{answered_questions[str(message.from_user.id)]}. {text} \n"

        try:
            response = requests.get(edited_url)
            current_data = response.json()
        except requests.RequestException as e:
            await message.answer(f"Xato: Server bilan bog'lanishda xato: {e}")
            return

        data = {
            "juda_ham_qoniqaman": current_data.get("juda_ham_qoniqaman", 0),
            "ortacha_qoniqaman": current_data.get("ortacha_qoniqaman", 0),
            "asosan_qoniqaman": current_data.get("asosan_qoniqaman", 0),
            "qoniqmayman": current_data.get("qoniqmayman", 0),
            "umuman_qoniqaman": current_data.get("umuman_qoniqaman", 0)
        }

        if text == "Juda yaxshi":
            data["juda_ham_qoniqaman"] += 1
        elif text == "Yaxshi":
            data["ortacha_qoniqaman"] += 1
        elif text == "O'rtacha":
            data["asosan_qoniqaman"] += 1
        elif text == "Past":
            data["qoniqmayman"] += 1
        elif text == "Yomon":
            data["umuman_qoniqaman"] += 1  

        try:
            response = requests.put(edited_url, json=data)
            if response.status_code != 200:
                await message.answer(f"Xato: Ma'lumotlarni yangilashda xato. Kod: {response.status_code}")
                return
        except requests.RequestException as e:
            await message.answer(f"Xato: Server bilan bog'lanishda xato: {e}")
            return

        await message.answer(f"<b>{queastions[answered_questions[str(message.from_user.id)]-1]}</b>",parse_mode="html",reply_markup=reply_kb_3)

        answered_questions[str(message.from_user.id)] += 1
    elif answered_questions[str(message.from_user.id)] == 7:

        await message.react([types.ReactionTypeEmoji(emoji='⚡️')])

        teacher_name = answered_questions[message.from_user.username].strip()
        teacher_telegram_id = get_teacher_telegram_id(teacher_name)

        teacher_id = get_teacher_id(answered_questions[message.from_user.username])
        total_answer += "</pre>"

        await message.answer(total_answer, parse_mode="html")

        if teacher_telegram_id:
            text = await get_teacher_status(teacher_id)
            await bot.send_message(chat_id=teacher_telegram_id, text=text, parse_mode="html")