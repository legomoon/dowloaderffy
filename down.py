from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess
import os

BOT_TOKEN = '7568707247:AAG6B0KHQ023bziF76ivCKVWLf6lHRyLL8c'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک موزیک رو بفرست (Spotify یا YouTube) 🎶")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("لینک معتبر بفرست 😐")
        return

    await update.message.reply_text("در حال دانلود موزیک... ⏳")

    try:
        # استفاده از SpotDL برای گرفتن موزیک از اسپاتیفای (درواقع یوتیوب)
        subprocess.run(["spotdl", url], check=True)

        # پیدا کردن فایل MP3 دانلود شده
        for file in os.listdir():
            if file.endswith(".mp3"):
                with open(file, 'rb') as f:
                    await update.message.reply_audio(audio=f)
                os.remove(file)  # حذف فایل بعد از ارسال
                break
        else:
            await update.message.reply_text("نتونستم فایل موزیک رو پیدا کنم 😞")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"خطا در دانلود موزیک 🚫\n{e}")
    except Exception as e:
        await update.message.reply_text(f"مشکلی پیش اومده 😵\n{e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

app.run_polling()
