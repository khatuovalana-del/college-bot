import logging
import asyncio
import os
from datetime import datetime, date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# ===== НАСТРОЙКИ =====
TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== ЗВОНКИ =====
TIME = ["9:00–10:00", "10:05–11:05", "11:20–12:20", "12:25–13:25"]

# ===== ЧИСЛИТЕЛЬ И ЗНАМЕНАТЕЛЬ =====
NUMERATOR = [
    ("2026-09-01", "2026-09-04"), ("2026-09-14", "2026-09-18"),
    ("2026-09-28", "2026-10-02"), ("2026-10-12", "2026-10-16"),
    ("2026-10-26", "2026-10-30"), ("2026-11-09", "2026-11-13"),
    ("2026-11-23", "2026-11-27"), ("2026-12-07", "2026-12-11"),
    ("2026-12-21", "2026-12-25"),
]

DENOMINATOR = [
    ("2026-09-07", "2026-09-11"), ("2026-09-21", "2026-09-25"),
    ("2026-10-05", "2026-10-09"), ("2026-10-19", "2026-10-23"),
    ("2026-11-02", "2026-11-06"), ("2026-11-16", "2026-11-20"),
    ("2026-11-30", "2026-12-04"), ("2026-12-14", "2026-12-18"),
]

def get_week_type():
    today = date.today()
    for start, end in NUMERATOR:
        if datetime.strptime(start, "%Y-%m-%d").date() <= today <= datetime.strptime(end, "%Y-%m-%d").date():
            return "числитель"
    for start, end in DENOMINATOR:
        if datetime.strptime(start, "%Y-%m-%d").date() <= today <= datetime.strptime(end, "%Y-%m-%d").date():
            return "знаменатель"
    return None

# ===== РАСПИСАНИЕ =====
SCHEDULE = {
    "Юриспруденция": {
        0: [("Химия (Болурова Ф.И.)", "География (Алиев Р.У.)"),
            ("Иностранный язык (Гочияева З.Р.)", "География (Алиев Р.У.)"),
            ("Физическая культура (Чагаров Р.Б.)",),
            ("Обществознание (Хасанова А.Л.)",)],
        1: [("Иностранный язык (Гочияева З.Р.)",),
            ("Химия (Болурова Ф.И.)",),
            ("Химия (Болурова Ф.И.)",),
            ("История (Хапаева Ф.З.)",)],
        2: [("Русский язык (Бедраева Ф.М.)",),
            ("Ин. язык (Гочияева З.Р.)", "Осн.проект.деят. (Боташев Т.М.)"),
            ("Физика (Боташев Т.М.)",),
            ("Обществознание (Хасанова А.Л.)",)],
        3: [("Математика (Булатова Э.М.)",),
            ("Информатика (Боташев Т.М.)",),
            ("Математика (Булатова Э.М.)",),
            ("Математика (Булатова Э.М.)",)],
        4: [("История (Хапаева Ф.З.)", "Физика (Боташев Т.М.)"),
            ("Информатика (Боташев Т.М.)",),
            ("-",), ("-",)],
    },
    "Операторы": {
        0: [("Математика (Булатова Э.М.)", "Ин.яз (Гочияева З.Р.)"),
            ("Иностранный язык (Гочияева З.Р.)",),
            ("Информатика (Боташев Т.М.)",),
            ("Биология (Болурова Ф.И.)",)],
        1: [("Русский язык (Бедраева Ф.М.)", "Биология (Болурова Ф.И.)"),
            ("Химия (Болурова Ф.И.)",),
            ("Обществознание (Хасанова А.Л.)",),
            ("История (Хапаева Ф.З.)",)],
        2: [("Математика (Булатова Э.М.)",),
            ("Ин.яз (Гочияева З.Р.)", "Осн.проект.деят. (Боташев Т.М.)"),
            ("ОБЗР (Чагаров Р.Б.)",),
            ("Физика (Боташев Т.М.)",)],
        3: [("Физика (Боташев Т.М.)",),
            ("Литература (Бедраева Ф.М.)",),
            ("История (Хапаева Ф.З.)",),
            ("-",)],
        4: [("Осн.пр.деят. (Боташев Т.М.)", "Литература (Бедраева Ф.М.)"),
            ("Информатика (Боташев Т.М.)",),
            ("Физическая культура (Чагаров Р.Б.)",),
            ("-",)],
    },
    "Медицинский — 1 группа": {
        0: [("Информатика (Боташев Т.М.)",),
            ("Биология (Болурова Ф.И.)",),
            ("Химия (Болурова Ф.И.)",),
            ("Иностранный язык (Гочияева З.Р.)",)],
        1: [("Химия (Болурова Ф.И.)", "География (Алиев Р.У.)"),
            ("Физика (Боташев Т.М.)",),
            ("Математика (Булатова Э.М.)",),
            ("Физическая культура (Чагаров Р.Б.)",)],
        2: [("Химия (Болурова Ф.И.)",),
            ("Русский язык (Бедраева Ф.М.)",),
            ("Обществознание (Хасанова А.Л.)",),
            ("Биология (Болурова Ф.И.)",)],
        3: [("Родная литература (Бедраева Ф.М.)",),
            ("История (Хапаева Ф.З.)",),
            ("ОБЗР (Чагаров Р.Б.)",),
            ("-",)],
        4: [("Литература (Бедраева Ф.М.)",),
            ("Инд. проект / Биология (Болурова Ф.И.)", "-"),
            ("История (Хапаева Ф.З.)",),
            ("-",)],
    },
    "Медицинский — 2 группа": {
        0: [("Литература (Бедраева Ф.М.)",),
            ("Русский язык (Бедраева Ф.М.)",),
            ("Литература (Бедраева Ф.М.)", "География (Алиев Р.У.)"),
            ("-",)],
        1: [("Физика (Боташев Т.М.)",),
            ("Родная литература (Бедраева Ф.М.)",),
            ("ОБЗР (Чагаров Р.Б.)",),
            ("Обществознание (Хасанова А.Л.)",)],
        2: [("Иностранный язык (Гочияева З.Р.)",),
            ("Биология (Болурова Ф.И.)",),
            ("Химия (Болурова Ф.И.)",),
            ("Физическая культура (Чагаров Р.Б.)",)],
        3: [("Химия (Болурова Ф.И.)",),
            ("Биология (Болурова Ф.И.)",),
            ("Информатика (Боташев Т.М.)",),
            ("История (Хапаева Ф.З.)",)],
        4: [("Инд. проект / Биология (Болурова Ф.И.)",),
            ("История (Хапаева Ф.З.)",),
            ("Математика (Булатова Э.М.)",),
            ("-",)],
    },
}

DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

def faculty_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⚙️ Операторы", callback_data="fac:Операторы"))
    builder.add(InlineKeyboardButton(text="⚖️ Юриспруденция", callback_data="fac:Юриспруденция"))
    builder.add(InlineKeyboardButton(text="🩺 Медицинский — 1 группа", callback_data="fac:Медицинский — 1 группа"))
    builder.add(InlineKeyboardButton(text="🩺 Медицинский — 2 группа", callback_data="fac:Медицинский — 2 группа"))
    builder.adjust(1)
    return builder.as_markup()

def days_kb(faculty):
    builder = InlineKeyboardBuilder()
    for i, day in enumerate(DAYS):
        builder.add(InlineKeyboardButton(text=day, callback_data=f"day:{faculty}:{i}"))
    builder.add(InlineKeyboardButton(text="📅 Вся неделя", callback_data=f"week:{faculty}"))
    builder.add(InlineKeyboardButton(text="🔙 Сменить факультет", callback_data="back"))
    builder.adjust(2, 2, 1, 1, 1)
    return builder.as_markup()

def format_pair(pair_tuple, week_type):
    if len(pair_tuple) == 1:
        return pair_tuple[0]
    num, den = pair_tuple[0], pair_tuple[1]
    if week_type == "числитель":
        return num if num != "-" else den
    elif week_type == "знаменатель":
        return den if den != "-" else num
    else:
        if num == "-":
            return den
        if den == "-":
            return num
        return f"{num} / {den}"

def format_day(faculty, day_index):
    week_type = get_week_type()
    pairs = SCHEDULE[faculty][day_index]
    text = f"📚 <b>{faculty}</b>\n📅 <b>{DAYS[day_index]}</b>\n"
    if week_type:
        text += f"🗓 <i>Неделя: {week_type}</i>\n"
    text += "\n"
    has_pairs = False
    for i, pair in enumerate(pairs):
        subject = format_pair(pair, week_type)
        if subject == "-":
            continue
        has_pairs = True
        text += f"<b>{i+1} пара</b> ({TIME[i]}): {subject}\n"
    if not has_pairs:
        text += "Пар нет 🎉"
    return text

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\nЯ помощник студента колледжа.\nВыбери свой факультет:",
        reply_markup=faculty_kb()
    )

@dp.callback_query(F.data.startswith("fac:"))
async def choose_faculty(call: types.CallbackQuery):
    faculty = call.data.split(":", 1)[1]
    await call.message.edit_text(
        f"Ты выбрал: <b>{faculty}</b>\nВыбери день недели:",
        reply_markup=days_kb(faculty), parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("day:"))
async def show_day(call: types.CallbackQuery):
    parts = call.data.split(":", 2)
    faculty = parts[1]
    day_index = int(parts[2])
    text = format_day(faculty, day_index)
    await call.message.edit_text(text, reply_markup=days_kb(faculty), parse_mode="HTML")

@dp.callback_query(F.data.startswith("week:"))
async def show_week(call: types.CallbackQuery):
    faculty = call.data.split(":", 1)[1]
    week_type = get_week_type()
    text = f"📚 <b>{faculty}</b> — расписание на неделю\n"
    if week_type:
        text += f"🗓 <i>Неделя: {week_type}</i>\n"
    text += "\n"
    for d in range(5):
        text += f"📅 <b>{DAYS[d]}</b>\n"
        for i, pair in enumerate(SCHEDULE[faculty][d]):
            subject = format_pair(pair, week_type)
            if subject == "-":
                continue
            text += f"  {i+1}. {TIME[i]} — {subject}\n"
        text += "\n"
    await call.message.edit_text(text, reply_markup=days_kb(faculty), parse_mode="HTML")

@dp.callback_query(F.data == "back")
async def back(call: types.CallbackQuery):
    await call.message.edit_text("Выбери факультет:", reply_markup=faculty_kb())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
