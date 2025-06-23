from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from langdetect import detect

TOKEN = "8186499354:AAFXwqw28hhPqWwnZBdNT5ZTG3LD-FJaBaU"

# 多语言自动回复字典
REPLIES = {
    "greeting": {
        "en": "Hello! How can I help you?",
        "es": "¡Hola! ¿En qué puedo ayudarte?",
        "zh-tw": "你好呀，有什麼我可以幫忙的？",
        "ja": "こんにちは！何かお手伝いできますか？",
        "ko": "안녕하세요! 무엇을 도와드릴까요?"
    },
    "price": {
        "en": "Which coin price are you interested in?",
        "es": "¿Qué moneda quieres consultar?",
        "zh-tw": "您想查詢哪一種幣的價格？",
        "ja": "どのコインの価格を知りたいですか？",
        "ko": "어떤 코인의 가격을 알고 싶으신가요?"
    },
    "default": {
        "en": "Sorry, I don't understand yet.",
        "es": "Lo siento, todavía no entiendo.",
        "zh-tw": "抱歉，我還聽不懂這句話。",
        "ja": "すみません、まだ理解できません。",
        "ko": "죄송합니다. 아직 이해하지 못했어요."
    }
}

# 自动文本回复
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    lang = detect(msg)
    msg_lower = msg.lower()

    if any(word in msg_lower for word in ["hello", "hola", "你好"]):
        reply = REPLIES["greeting"].get(lang, REPLIES["greeting"]["en"])
    elif any(word in msg_lower for word in ["price", "precio", "價格", "价格"]):
        reply = REPLIES["price"].get(lang, REPLIES["price"]["en"])
    else:
        reply = REPLIES["default"].get(lang, REPLIES["default"]["en"])

    await update.message.reply_text(reply)

# /help 指令回复
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Huobi Assistant Bot Help*\n\n"
        "/start – Begin interacting with the bot\n"
        "/price – Check real-time prices (e.g., BTC, ETH)\n"
        "/lang – View supported languages\n"
        "/about – Learn more about this bot\n\n"
        "💬 You can also type keywords like 'hello', 'price', or a coin name.\n"
        "🌍 This bot supports English, Spanish, Chinese (Traditional), Japanese, and Korean."
    )
    await update.message.reply_markdown(help_text)

# 初始化应用
app = ApplicationBuilder().token(TOKEN).build()

# 注册处理器
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("✅ Huobi 多语言机器人已启动...")
app.run_polling()
