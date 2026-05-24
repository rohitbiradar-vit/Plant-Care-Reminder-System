import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import schedule
from datetime import date

# Custom imports
from reminder import get_reminders_text, get_season_tip, get_due_notifications
from file_handler import view_log, save_report
from raf_handler import read_all_plants
from plant_data import PLANT_PROFILES
from plant_manager import (
    add_plant_bot, 
    view_plants_bot, 
    log_care_task_bot, 
    delete_plant_bot, 
    search_plant_bot, 
    plant_statistics_bot
)

# ⚠️ REPLACE WITH YOUR ACTUAL BOT TOKEN
BOT_TOKEN = "8811179067:AAEynvLbsknKUqAwRbVvEqZ9RyJUobCFR0Y"
bot = telebot.TeleBot(BOT_TOKEN)
admin_chat_id = None 

# ==========================================
# CORE COMMANDS
# ==========================================

@bot.message_handler(commands=['start', 'help', 'menu'])
def send_menu(message):
    global admin_chat_id
    admin_chat_id = message.chat.id
    
    menu_text = (
        "🌿 *PLANT CARE REMINDER SYSTEM* 🌿\n\n"
        "Here is your main menu:\n"
        "/add - 🌱 Add a new plant\n"
        "/plants - 🪴 View all plants\n"
        "/log - ✅ Log a care task\n"
        "/reminders - 🔔 Check reminders\n"
        "/history - 📋 View task history\n"
        "/delete - 🗑️ Delete a plant\n"
        "/search - 🔍 Search plant\n"
        "/stats - 📊 Plant statistics\n"
        "/report - 📁 Generate health report\n"
    )
    bot.reply_to(message, menu_text, parse_mode='Markdown')

@bot.message_handler(commands=['plants'])
def handle_view_plants(message):
    bot.reply_to(message, view_plants_bot(), parse_mode='Markdown')

@bot.message_handler(commands=['reminders'])
def handle_reminders(message):
    bot.reply_to(message, get_reminders_text(), parse_mode='Markdown')

@bot.message_handler(commands=['history'])
def handle_history(message):
    history = view_log()
    bot.reply_to(message, f"📋 *TASK HISTORY*\n\n{history}", parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def handle_stats(message):
    bot.reply_to(message, plant_statistics_bot(), parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def handle_report(message):
    plants = read_all_plants()
    if not plants:
        bot.reply_to(message, "⚠️ No plants to export!")
        return

    today = date.today()
    season, tip = get_season_tip()
    
    report_content = f"🌿 PLANT CARE HEALTH REPORT 🌿\nGenerated: {today}\nSeason: {season}\nTip: {tip}\n\n"
    for p in plants:
        report_content += f"Plant: {p['name']} (ID: {p['id']}) | Species: {p['species']}\n"
    
    save_report(report_content)
    
    with open("report.txt", "rb") as file:
        bot.send_document(message.chat.id, file, caption="📁 Here is your latest Plant Health Report!")

# ==========================================
# INTERACTIVE MULTI-STEP COMMANDS
# ==========================================

# --- ADD PLANT (With Buttons & Auto-Naming) ---
@bot.message_handler(commands=['add'])
def start_add(message):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    
    for key, profile in PLANT_PROFILES.items():
        if key != "default":
            buttons.append(InlineKeyboardButton(profile["common_name"], callback_data=f"add_{key}"))
            
    markup.add(*buttons)
    bot.reply_to(message, "🌱 Let's add a plant! First, choose a species from our database:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def process_add_species_selection(call):
    species_key = call.data.split('_')[1]
    species_name = PLANT_PROFILES[species_key]["common_name"]

    bot.answer_callback_query(call.id, f"Selected: {species_name}")

    msg = bot.send_message(call.message.chat.id, f"Great choice: *{species_name}*! 🌿\n\nNow, enter a unique *Plant ID* (e.g., 007):", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_add_id, species_key)

def process_add_id(message, species_key):
    plant_id = message.text.strip()
    # Automatically use the species common name as the plant's name
    name = PLANT_PROFILES[species_key]["common_name"]
    # Save the plant directly!
    bot.reply_to(message, add_plant_bot(plant_id, name, species_key), parse_mode='Markdown')

# --- LOG TASK ---
@bot.message_handler(commands=['log'])
def start_log(message):
    msg = bot.reply_to(message, "✅ Enter the *Plant ID* you want to log a task for:", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_log_id)

def process_log_id(message):
    plant_id = message.text.strip()
    msg = bot.reply_to(message, "Which task did you do?\n(watering / fertilizing / pruning / pest\\_check / repotting)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_log_task, plant_id)

def process_log_task(message, plant_id):
    task = message.text.strip().lower()
    bot.reply_to(message, log_care_task_bot(plant_id, task), parse_mode='Markdown')

# --- SEARCH & DELETE ---
@bot.message_handler(commands=['search'])
def start_search(message):
    msg = bot.reply_to(message, "🔍 Enter the *Plant ID* to search:")
    bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, search_plant_bot(m.text.strip()), parse_mode='Markdown'))

@bot.message_handler(commands=['delete'])
def start_delete(message):
    msg = bot.reply_to(message, "🗑️ Enter the *Plant ID* you want to DELETE:")
    bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, delete_plant_bot(m.text.strip()), parse_mode='Markdown'))


# ==========================================
# AUTOMATED SMART REMINDERS
# ==========================================
def send_daily_push():
    if admin_chat_id:
        # Call our new smart alert function
        notification = get_due_notifications()
        
        # Only send a message to Telegram IF there is actually something due!
        if notification:
            bot.send_message(admin_chat_id, notification, parse_mode='Markdown')

def run_scheduler():
    schedule.every().day.at("20:35").do(send_daily_push)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("🌿 Telegram Bot is running! Press Ctrl+C to stop.")
    threading.Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling()