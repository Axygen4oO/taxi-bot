import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
Ты консультант для водителей Яндекс Такси.

Отвечай только по теме:
- Яндекс Про
- рейтинг
- активность
- приоритет
- фотоконтроль
- бонусы
- выплаты
- работа с пассажирами

Отвечай простым языком.
"""

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    prompt = f"""
{SYSTEM_PROMPT}

Вопрос:

{question}
"""

    response = model.generate_content(prompt)

    await update.message.reply_text(
        response.text[:4096]
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        answer
    )
)

print("Bot started")

app.run_polling()
