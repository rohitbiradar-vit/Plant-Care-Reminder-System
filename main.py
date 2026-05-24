from plant_manager import add_plant, view_plants, log_care_task, delete_plant, search_plant, plant_statistics
from reminder import check_reminders, get_season_tip
from file_handler import view_log, save_report
from datetime import date, datetime
import time

from plant_data import get_plant_profile
from datetime import date

def make_plant(pid, name, species):
    today   = str(date.today())
    profile = get_plant_profile(species)
    return {
        "id":      pid,
        "name":    name,
        "species": species,
        "tips":    profile["tips"],
        "care_tasks": {
            task: {"every_days": days, "last_done": today}
            for task, days in profile["care_tasks"].items()
        }
    }

DEFAULT_PLANTS = [
    make_plant("001", "Rose 1",   "rosa"),
    make_plant("002", "Rose 2",   "rosa"),
    make_plant("003", "Cactus 1", "cactaceae"),
    make_plant("004", "Aloe 1",   "aloe vera"),
    make_plant("005", "Monstera", "monstera"),
]

def load_default_plants():
    plants = load_plants()
    if not plants:
        save_plants(DEFAULT_PLANTS)
        print("  ✅ Sample plants loaded automatically!")

def print_banner():
    print("""
    ╔══════════════════════════════════════╗
    ║   🌿  PLANT CARE REMINDER SYSTEM 🌿  ║
    ║        Keep Your Plants Happy!        ║
    ╚══════════════════════════════════════╝
    """)

def print_menu():
    print("\n  ┌─────────────────────────────────┐")
    print("  │           MAIN MENU             │")
    print("  ├─────────────────────────────────┤")
    print("  │  1. 🌱 Add a new plant          │")
    print("  │  2. 🪴 View all plants          │")
    print("  │  3. ✅ Log a care task          │")
    print("  │  4. 🔔 Check reminders          │")
    print("  │  5. 📋 View task history        │")
    print("  │  6. 🗑️  Delete a plant          │")
    print("  │  7. 🔍 Search plant             │")
    print("  │  8. 📊 Plant statistics         │")
    print("  │  9. 📁 Export health report     │")
    print("  │  0. 🚪 Exit                     │")
    print("  └─────────────────────────────────┘")

def loading(message):
    print(f"\n  {message}", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

def export_report():
    plants = load_plants()
    if not plants:
        print("  ⚠️  No plants to export!")
        return

    today        = date.today()
    season, tip  = get_season_tip()
    lines        = []

    lines.append("=" * 50)
    lines.append("       🌿 PLANT CARE HEALTH REPORT 🌿")
    lines.append("=" * 50)
    lines.append(f"  Generated On : {today}")
    lines.append(f"  Season       : {season}")
    lines.append(f"  Tip          : {tip}")
    lines.append("=" * 50)

    for p in plants:
        lines.append(f"\n  Plant   : {p['name']}  (ID: {p['id']})")
        lines.append(f"  Species : {p['species']}")
        for task, info in p["care_tasks"].items():
            last      = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            days_left  = info["every_days"] - days_since
            status     = ("OVERDUE!" if days_left < 0
                          else "DUE TODAY" if days_left == 0
                          else f"due in {days_left} day(s)")
            lines.append(f"  {task:<12}: {status}")
        lines.append("  " + "-" * 45)

    lines.append("\n" + "=" * 50)
    lines.append("         END OF REPORT")
    lines.append("=" * 50)

    save_report("\n".join(lines))
    print("\n  ✅ Report exported to report.txt!")

def main():
    print_banner()
    load_default_plants()
    time.sleep(1)
    while True:
        print_menu()
        choice = input("\n  👉 Enter your choice (0-9): ")

        if choice == "1":
            loading("Adding plant")
            add_plant()
        elif choice == "2":
            loading("Fetching plants")
            view_plants()
        elif choice == "3":
            loading("Logging task")
            log_care_task()
        elif choice == "4":
            loading("Checking reminders")
            check_reminders()
        elif choice == "5":
            loading("Loading history")
            print(view_log())
        elif choice == "6":
            loading("Deleting plant")
            delete_plant()
        elif choice == "7":
            loading("Searching")
            search_plant()
        elif choice == "8":
            loading("Loading statistics")
            plant_statistics()
        elif choice == "9":
            loading("Generating report")
            export_report()
        elif choice == "0":
            print("\n  🌿 Goodbye! Take care of your plants!\n")
            break
        else:
            print("\n  ❌ Invalid choice, try again!")

main()
