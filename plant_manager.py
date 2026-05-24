from raf_handler import *
from file_handler import log_task, get_task_count
from datetime import date, datetime
from plant_data import get_plant_profile

def add_plant_bot(plant_id, name, species):
    plants = read_all_plants()
    for p in plants:
        if p["id"].lower() == plant_id.lower():
            return "❌ Plant ID already exists! Please try again with a different ID."

    today = str(date.today())
    profile = get_plant_profile(species)
    
    care_tasks = {
        task: {"every_days": days, "last_done": today}
        for task, days in profile["care_tasks"].items()
    }

    plant = {
        "id": plant_id,
        "name": name,
        "species": species,
        "tips": profile["tips"],
        "care_tasks": care_tasks
    }

    slot = get_total_slots()
    write_plant(slot, plant)
    
    # Generate the rich success message with the full schedule
    msg = (f"✅ *{name}* added successfully!\n"
           f"🌿 ID: `{plant_id}`\n\n"
           f"📋 *Care Schedule:*\n")
    
    for task, info in care_tasks.items():
        clean_task = task.replace('_', ' ').title()
        msg += f"  - {clean_task}: every {info['every_days']} days\n"
        
    msg += f"\n💡 *Tip:* {profile['tips']}"
    
    return msg

def view_plants_bot():
    plants = read_all_plants()
    if not plants:
        return "⚠️ No plants registered yet."

    msg = f"🪴 *YOU HAVE {len(plants)} PLANT(S)*\n\n"
    for p in plants:
        msg += f"🌿 *ID: {p['id']}* - {p['name']} ({p['species']})\n"
        for task, info in p["care_tasks"].items():
            clean_task = task.replace('_', ' ').title()
            msg += f"  - {clean_task}: every {info['every_days']} days\n"
        msg += "━━━━━━━━━━━━━━━━━━\n"
    return msg

def log_care_task_bot(plant_id, task):
    plant, slot = find_plant_by_id(plant_id)
    if not plant:
        return "❌ Plant not found!"

    if task in plant["care_tasks"]:
        today = str(date.today())
        plant["care_tasks"][task]["last_done"] = today
        update_plant(slot, plant)
        log_task(plant["id"], plant["name"], task, today)
        return f"✅ '{task.replace('_', ' ').title()}' logged for {plant['name']}!"
    return "❌ Invalid task! Use: watering, fertilizing, pruning, pest_check, or repotting."

def delete_plant_bot(plant_id):
    plant, slot = find_plant_by_id(plant_id)
    if not plant:
        return "❌ Plant not found!"
    delete_plant_raf(slot)
    return f"🗑️ ✅ Plant '{plant['name']}' (ID: {plant_id}) deleted successfully!"

def search_plant_bot(plant_id):
    plant, slot = find_plant_by_id(plant_id)
    if not plant:
        return "❌ Plant not found!"
    
    msg = f"🔍 *PLANT FOUND (Slot {slot})*\n\n"
    msg += f"🌿 ID: {plant['id']}\nName: {plant['name']}\nSpecies: {plant['species']}\n\n"
    for task, info in plant["care_tasks"].items():
        msg += f"  - {task.replace('_', ' ').title()}: every {info['every_days']} days\n"
    return msg

def plant_statistics_bot():
    plants = read_all_plants()
    if not plants:
        return "⚠️ No plants registered yet."

    today = date.today()
    msg = f"📊 *PLANT STATISTICS*\nTotal Plants: {len(plants)}\n━━━━━━━━━━━━━━━━━━\n"

    for p in plants:
        msg += f"\n🌿 *{p['name']}* [{p['id']}]\n"
        for task, info in p["care_tasks"].items():
            count = get_task_count(p["id"], task)
            last = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            clean_task = task.replace('_', ' ').title()
            msg += f"  - {clean_task}: done {count}x (last {days_since} days ago)\n"
    return msg