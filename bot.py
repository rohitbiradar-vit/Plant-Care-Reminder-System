import telebot
import time
import threading
import schedule
from reminder import get_reminders_text
from file_handler import load_plants, load_default_plants

# Replace with your actual bot token from BotFather
BOT_TOKEN = "8811179067:AAEynvLbsknKUqAwRbVvEqZ9RyJUobCFR0Y"
bot = telebot.TeleBot(BOT_TOKEN)

# Store the Chat ID so the bot knows where to send automated daily reminders
# (You will get this ID the first time you interact with the bot)
admin_chat_id = None 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global admin_chat_id
    admin_chat_id = message.chat.id
    
    welcome_text = (
        "🌿 *PLANT CARE REMINDER SYSTEM* 🌿\n\n"
        "Welcome! Here are your commands:\n"
        "/plants - View all registered plants\n"
        "/reminders - Check current task statuses\n"
        "/log - Log a care task (e.g., watering)\n"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['reminders'])
def send_reminders(message):
    # Calls your newly modified function
    reminders = get_reminders_text() 
    bot.reply_to(message, reminders, parse_mode='Markdown')

# --- AUTOMATED DAILY REMINDER SYSTEM ---

def send_daily_push():
    if admin_chat_id:
        reminders = get_reminders_text()
        bot.send_message(admin_chat_id, f"🌅 *Daily Plant Update!*\n\n{reminders}", parse_mode='Markdown')

def run_scheduler():
    # Schedule the reminder to send every day at 8:00 AM
    schedule.every().day.at("08:00").do(send_daily_push)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    load_default_plants()
    print("🌿 Telegram Bot is running...")
    
    # Start the daily scheduler in a background thread
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Start listening for messages from Telegram
    bot.infinity_polling()