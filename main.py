
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
from threading import Thread
import random
from datetime import datetime, timezone
import asyncio
import os

TOKEN = os.getenv("TOKEN")
PASSWORD = "BDALAMIN"
channels = []
signal_on = False
adding_channel = False
awaiting_password = False

# Flask keep-alive
app = Flask(__name__)
@app.route('/')
def home():
    return "HGZY Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📡 SIGNAL ON", "🔌 SIGNAL OFF"], ["➕ ADD CHANNEL", "📋 CHANNEL LIST"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "<b>💢 𝐇𝐆𝐙𝐘 𝐀𝐔𝐓𝐎 𝐏𝐑𝐄𝐃𝐈𝗖𝗧𝗜𝗢𝗡 💢</b>

"
        "🚨 আমাদের বটে আপনাকে স্বাগতম আপনি এই বোট এর মাধ্যমে অটোমেটিক আপনার চ্যানেলে সিগনাল নিতে পারবেন।",
        parse_mode="HTML", reply_markup=markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global signal_on, channels, adding_channel, awaiting_password
    msg = update.message.text

    if msg == "📡 SIGNAL ON":
        signal_on = True
        await update.message.reply_text("✅ Signal system turned ON.")
    elif msg == "🔌 SIGNAL OFF":
        signal_on = False
        await update.message.reply_text("❌ Signal system turned OFF.")
    elif msg == "➕ ADD CHANNEL":
        awaiting_password = True
        await update.message.reply_text("🔐 ENTER PASSWORD TO ADD CHANNEL")
    elif awaiting_password:
        if msg.strip() == PASSWORD:
            awaiting_password = False
            adding_channel = True
            await update.message.reply_text("⛔ ENTER YOUR CHANNEL LINK ⬇️")
        else:
            awaiting_password = False
            await update.message.reply_text("❗ WRONG PASSWORD! ACCESS DENIED ❌")
    elif adding_channel:
        if msg.startswith("https://t.me/"):
            ch = "@" + msg.split("/")[-1]
        elif msg.startswith("@"):
            ch = msg
        else:
            ch = "@" + msg
        channels.append(ch)
        adding_channel = False
        await update.message.reply_text("🔴 CHANNEL ADDED SUCCESSFULLY ✅")
    elif msg == "📋 CHANNEL LIST":
        if not channels:
            await update.message.reply_text("ℹ️ No channel added yet.")
        else:
            text = "🔘 ALL CHANNEL LINK ⬇️\n\n"
            for c in channels:
                text += f"CHANNEL LINK ———> {c}\n"
            await update.message.reply_text(text)

# Prediction system
async def prediction_loop(app):
    while True:
        if signal_on and channels:
            now = datetime.now(timezone.utc)
            period = now.strftime("%Y%m%d") + "1000" + str(now.hour * 60 + now.minute)
            number = str(random.randint(0, 9))
            size = "𝐁𝐈𝐆" if int(number) >= 5 else "𝐒𝐌𝐀𝐋𝐋"
            color = random.choice(["🔴", "🟢"])
            msg = (
                "<b>💢 𝗛𝗚𝗭𝗬 𝗔𝗨𝗧𝗢 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗜𝗢𝗡 💢</b>\n\n"
                f"⏳ 𝙿𝙴𝚁𝙸𝙾𝙳 𝙸𝙳 : <b>{period}</b>\n\n"
                f"🚨 𝚁𝙴𝚂𝚄𝙻𝚃 --> {size} {color} <b>{number}</b>\n\n"
                "⭕ ᗰᑌՏT ᗷᗴ 7-8 ՏTᗴᑭ ᗰᗩIᑎTᗩIᑎ."
            )
            for ch in channels:
                try:
                    await app.bot.send_message(chat_id=ch, text=msg, parse_mode="HTML")
                except Exception as e:
                    print(f"Send Error: {e}")
        await asyncio.sleep(60)

# Start bot
async def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.create_task(prediction_loop(app))
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
