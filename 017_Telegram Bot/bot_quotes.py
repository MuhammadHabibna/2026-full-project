import telebot
import random

# ========================================
# TELEGRAM BOT (QUOTE & JOKE) - DAY 17
# ========================================

# ⚠️ GANTI TOKEN INI DENGAN TOKEN DARI @BotFather
TOKEN = 'GANTI_DENGAN_TOKEN_BOT_ANDA'

try:
    bot = telebot.TeleBot(TOKEN)
except:
    print(f"[ERROR] Token belum diisi! Edit file ini dan masukkan token dari BotFather.")
    # Dummy object biar ga error syntax saat dijalankan tanpa token
    bot = type('obj', (object,), {'message_handler': lambda *a, **k: lambda f: f, 'infinity_polling': lambda: None})


# DATA JOKES & QUOTES
QUOTES = [
    "“The only way to do great work is to love what you do.” – Steve Jobs",
    "“Code is like humor. When you have to explain it, it’s bad.” – Cory House",
    "“First, solve the problem. Then, write the code.” – John Johnson",
    "“Experience is the name everyone gives to their mistakes.” – Oscar Wilde",
    "“Simplicity is the soul of efficiency.” – Austin Freeman"
]

JOKES = [
    "Kenapa programmer nggak suka alam? Karena banyak bugs.",
    "Apa bedanya Hardware dan Software? Hardware bisa ditendang, Software cuma bisa dimaki.",
    "0 adalah false, 1 adalah true, selain itu... error.",
    "Programmer itu seperti mesin kopi: Input Kopi -> Output Code.",
    "Kenapa komputer kedinginan? Karena Windows-nya kebuka!"
]

print("🤖 BOT BERJALAN... Tekan Ctrl+C untuk berhenti.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya Bot Motivasi & Humor 🤖\n\nKetik:\n/quote - Untuk kata bijak\n/joke - Untuk lelucon programming")

@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote = random.choice(QUOTES)
    bot.reply_to(message, f"💡 *QUOTE HARI INI:*\n\n{quote}", parse_mode='Markdown')

@bot.message_handler(commands=['joke'])
def send_joke(message):
    joke = random.choice(JOKES)
    bot.reply_to(message, f"😂 *JOKE RECEH:*\n\n{joke}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Maaf, saya cuma ngerti /quote dan /joke 😐")

if __name__ == "__main__":
    if TOKEN == 'GANTI_DENGAN_TOKEN_BOT_ANDA':
        print("\n[PENTING] Anda belum memasukkan Token Bot Telegram!")
        print("1. Buka Telegram -> Cari @BotFather")
        print("2. Ketik /newbot -> Ikuti langkahnya")
        print("3. Copy API Token -> Paste di variable TOKEN di baris 8")
    else:
        print("✅ Bot siap melayani! Coba chat bot di Telegram.")
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")

# CARA INSTALL:
# pip install pyTelegramBotAPI
