from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

BOT_TOKEN = "8295347595:AAHJoqEoLzvLFC9PPQGOFP60_TfKelYjrqM"
ADMIN_ID = 7636706065
CHANNEL_ID = "2526848610"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send /feedback <your message> or send media (photo/video/file) — it will be forwarded in 5 minutes."
    )

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❗ Use: /feedback your_message")
        return
    user = update.effective_user.mention_html()
    text = f"📩 Feedback from {user}:\n{msg}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode='HTML')
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML')
    await update.message.reply_text("✅ Feedback sent!")

async def delayed_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Media received! It will be forwarded in 5 minutes.")
    await asyncio.sleep(300)

    try:
        await update.message.copy(chat_id=ADMIN_ID)
        await update.message.copy(chat_id=CHANNEL_ID)
        await update.message.reply_text("✅ Media forwarded after 5 minutes.")
    except Exception as e:
        await update.message.reply_text("⚠️ Failed to forward media.")
        print("Error:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("feedback", feedback))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, delayed_forward))

                              

app.run_polling()
