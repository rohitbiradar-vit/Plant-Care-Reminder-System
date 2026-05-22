from file_handler import load_plants
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

def check_reminders():
    plants = load_plants()
    today  = date.today()
    season, tip = get_season_tip()

    print("\n  🔔 REMINDER CHECK")
    print("  " + "=" * 40)
    print(f"  📅 Date   : {today}")
    print(f"  🌦️  Season : {season}")
    print(f"  💡 Tip    : {tip}")
    print("  " + "=" * 40)

    for p in plants:
        print(f"\n  🌿 {p['name']} (ID: {p['id']})")
        for task, info in p["care_tasks"].items():
            last      = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            days_left  = info["every_days"] - days_since

            if days_left < 0:
                print(f"     ❌ {task:<12} — OVERDUE by {abs(days_left)} day(s)!")
            elif days_left == 0:
                print(f"     💧 {task:<12} — DUE TODAY!")
            elif days_left <= 2:
                print(f"     ⚠️  {task:<12} — due in {days_left} day(s)")
            else:
                print(f"     ✅ {task:<12} — due in {days_left} day(s)")

    print("\n  " + "=" * 40)