import telebot
import time
import threading
import schedule

# Import your custom functions from the other files
from reminder import get_reminders_text
from plant_manager import (
    get_plants_text, 
    log_care_task_bot, 
    suggest_watering, 
    add_plant_bot
)

# ⚠️ REPLACE THIS WITH YOUR ACTUAL BOT TOKEN FROM @BotFather
BOT_TOKEN = "8811179067:AAEynvLbsknKUqAwRbVvEqZ9RyJUobCFR0Y"
bot = telebot.TeleBot(BOT_TOKEN)

# Stores the chat ID so the bot knows where to send the automatic morning reminders
admin_chat_id = None 


# ==========================================
# BOT COMMANDS
# ==========================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global admin_chat_id
    admin_chat_id = message.chat.id # Saves your chat ID for daily pushes
    
    welcome_text = (
        "🌿 *PLANT CARE BOT* 🌿\n\n"
        "Welcome! Here are your commands:\n"
        "/plants - View all registered plants\n"
        "/reminders - Check task statuses\n"
        "/log - Log a care task\n"
        "/add - Add a new plant to your collection\n"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['plants'])
def send_plants(message):
    bot.reply_to(message, get_plants_text(), parse_mode='Markdown')

@bot.message_handler(commands=['reminders'])
def send_reminders(message):
    bot.reply_to(message, get_reminders_text(), parse_mode='Markdown')


# ==========================================
# /LOG COMMAND (Multi-step)
# ==========================================

@bot.message_handler(commands=['log'])
def start_logging(message):
    msg = bot.reply_to(message, "Reply with the *Plant ID* you want to update (e.g., a1b2):", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_plant_id_step)

def process_plant_id_step(message):
    plant_id = message.text.strip()
    # Notice the double backslash \\ before the underscore in pest_check!
    msg = bot.reply_to(message, f"Great. Now reply with the *task* done for ID {plant_id}:\n(watering / fertilizing / pruning / pest\\_check)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_task_step, plant_id)

def process_task_step(message, plant_id):
    task = message.text.strip().lower()
    result_text = log_care_task_bot(plant_id, task)
    bot.reply_to(message, result_text, parse_mode='Markdown')


# ==========================================
# /ADD COMMAND (Multi-step with Smart Suggestions)
# ==========================================

@bot.message_handler(commands=['add'])
def start_add_plant(message):
    msg = bot.reply_to(message, "🌱 What is the name of your new plant?")
    bot.register_next_step_handler(msg, process_add_name_step)

def process_add_name_step(message):
    plant_name = message.text.strip()
    suggested_days, species = suggest_watering(plant_name)

    text = (
        f"I see you're adding a *{plant_name}*!\n\n"
        f"Based on its name, I suggest watering every *{suggested_days} days*.\n\n"
        f"Do you want to use this schedule?\n"
        f"👉 Reply `yes` to accept, OR type a *number* (e.g., `5`) to set your own custom days."
    )
    msg = bot.reply_to(message, text, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_add_confirm_step, plant_name, species, suggested_days)

def process_add_confirm_step(message, plant_name, species, suggested_days):
    response = message.text.strip().lower()
    
    # Process user input (yes or custom number)
    if response in ['yes', 'y', 'ok', 'sure']:
        water_freq = suggested_days
    elif response.isdigit():
        water_freq = int(response)
    else:
        bot.reply_to(message, "❌ Invalid input. Please reply with `yes` or a number. Let's try again: type /add")
        return

    # Save to database using the function we added to plant_manager.py
    plant_id = add_plant_bot(plant_name, species, water_freq)
    
    success_text = (
        f"✅ *{plant_name}* added successfully!\n"
        f"🌿 Unique ID: `{plant_id}`\n"
        f"💧 Watering set to every {water_freq} days."
    )
    bot.reply_to(message, success_text, parse_mode='Markdown')


# ==========================================
# AUTOMATED DAILY REMINDER SYSTEM
# ==========================================

def send_daily_push():
    if admin_chat_id:
        reminders = get_reminders_text()
        bot.send_message(admin_chat_id, f"🌅 *Daily Plant Update!*\n\n{reminders}", parse_mode='Markdown')

def run_scheduler():
    # Sends the reminder every day at 8:00 AM
    schedule.every().day.at("08:00").do(send_daily_push)
    while True:
        schedule.run_pending()
        time.sleep(1)


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    print("🌿 Telegram Bot is running! Go to Telegram and send /start")
    
    # Run the daily scheduler in a background thread so it doesn't block the bot
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Start listening to Telegram messages
    bot.infinity_polling()