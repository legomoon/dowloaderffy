from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio

BOT_TOKEN = "7568707247:AAG6B0KHQ023bziF76ivCKVWLf6lHRyLL8c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک موزیک رو بفرست (Spotify یا YouTube) 🎶")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("لینک معتبر بفرست 😐")
        return

    await update.message.reply_text("در حال دانلود موزیک... ⏳")

    try:
        # اجرای spotdl بصورت async
        process = await asyncio.create_subprocess_exec(
            "spotdl", url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            await update.message.reply_text(f"خطا در دانلود موزیک 🚫\n{stderr.decode()}")
            return

        # پیدا کردن آخرین فایل mp3 ساخته شده در دایرکتوری فعلی
        mp3_files = [f for f in os.listdir() if f.endswith(".mp3")]
        if not mp3_files:
            await update.message.reply_text("نتونستم فایل موزیک رو پیدا کنم 😞")
            return

        latest_file = max(mp3_files, key=os.path.getctime)

        with open(latest_file, "rb") as f:
            await update.message.reply_audio(audio=f)

        os.remove(latest_file)  # حذف فایل بعد از ارسال

    except Exception as e:
        await update.message.reply_text(f"مشکلی پیش اومده 😵\n{e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()
