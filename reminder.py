from raf_handler import read_all_plants
from datetime import date, datetime

def get_season_tip():
    month = date.today().month
    if month in [3, 4, 5]:
        return "Spring", "Water regularly — plants are growing fast!"
    elif month in [6, 7, 8]:
        return "Summer", "Water more frequently — heat dries soil quickly!"
    elif month in [9, 10, 11]:
        return "Autumn", "Reduce watering — growth is slowing down."
    else:
        return "Winter", "Water sparingly — plants need very little now."

def get_reminders_text():
    plants = read_all_plants()
    if not plants:
        return "⚠️ No plants found in database."
        
    today  = date.today()
    season, tip = get_season_tip()

    lines = [
        "🔔 *REMINDER CHECK*",
        f"📅 Date: {today}",
        f"🌦️ Season: {season}",
        f"💡 Tip: {tip}",
        "━━━━━━━━━━━━━━━━━━━━"
    ]

    for p in plants:
        lines.append(f"\n🌿 *{p['name']}* (ID: {p['id']})")
        for task, info in p["care_tasks"].items():
            last = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            days_left  = info["every_days"] - days_since
            clean_task = task.replace('_', ' ').title()

            if days_left < 0:
                lines.append(f"  ❌ {clean_task} — OVERDUE by {abs(days_left)} day(s)!")
            elif days_left == 0:
                lines.append(f"  💧 {clean_task} — DUE TODAY!")
            elif days_left <= 2:
                lines.append(f"  ⚠️ {clean_task} — due in {days_left} day(s)")
            else:
                lines.append(f"  ✅ {clean_task} — due in {days_left} day(s)")

        return "\n".join(lines)

def get_due_notifications():
    """Checks for plants that need immediate attention and returns an alert string."""
    plants = read_all_plants()
    if not plants:
        return None
        
    today = date.today()
    alerts = []
    
    for p in plants:
        for task, info in p["care_tasks"].items():
            last = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            days_left = info["every_days"] - days_since
            
            clean_task = task.replace('_', ' ').title()
            
            if days_left < 0:
                alerts.append(f"🚨 *{p['name']}* (ID: {p['id']}) — {clean_task} is OVERDUE by {abs(days_left)} day(s)!")
            elif days_left == 0:
                alerts.append(f"💧 *{p['name']}* (ID: {p['id']}) — {clean_task} is DUE TODAY!")
    
    # If the alerts list is empty, it means no plants need care today!
    if not alerts:
        return None 
        
    # If there are alerts, format them nicely
    msg = "🔔 *PLANT CARE ALERT*\n━━━━━━━━━━━━━━━━━━\n"
    return msg + "\n".join(alerts)