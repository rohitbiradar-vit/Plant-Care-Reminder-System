from file_handler import load_plants, save_plants, log_task, get_task_count
from datetime import date, datetime
import uuid
from plant_data import get_plant_profile, PLANT_PROFILES

from plant_data import get_plant_profile, PLANT_PROFILES
def add_plant():

    print("\n  🌱 ADD NEW PLANT")
    print("  " + "-" * 35)

    # SHOW AVAILABLE SPECIES
    print("\n  🌿 Available Plant Profiles:")

    for key, value in PLANT_PROFILES.items():
        if key != "default":
            print(f"     → {value['common_name']} ({key})")

    print()

    # USER INPUT
    plant_id = input("  Plant ID      : ").strip()
    name     = input("  Plant name    : ").strip()
    species  = input("  Species       : ").strip().lower()

    today = str(date.today())

    # GET AUTOMATIC PROFILE
    profile = get_plant_profile(species)

    print(f"\n  ✅ Profile Found : {profile['common_name']}")
    print(f"  💡 Tip           : {profile['tips']}")

    print("\n  📋 AUTO CARE SCHEDULE")

    for task, days in profile["care_tasks"].items():
        print(f"     → {task:<12}: every {days} day(s)")

    # CREATE CARE TASKS AUTOMATICALLY
    care_tasks = {
        task: {
            "every_days": days,
            "last_done": today
        }
        for task, days in profile["care_tasks"].items()
    }

    # CREATE PLANT OBJECT
    plant = {
        "id": plant_id,
        "name": name,
        "species": species,
        "tips": profile["tips"],
        "care_tasks": care_tasks
    }

    # SAVE
    plants = load_plants()
    plants.append(plant)
    save_plants(plants)

    print(f"\n  ✅ {name} added successfully!")
def view_plants():
    plants = load_plants()
    if not plants:
        print("  ⚠️  No plants registered yet.")
        return
    print(f"\n  🪴 YOU HAVE {len(plants)} PLANT(S)\n")
    for p in plants:
        print("  ╔══════════════════════════════════╗")
        print(f"  🌿 ID      : {p['id']}")
        print(f"     Name    : {p['name']}")
        print(f"     Species : {p['species']}")
        for task, info in p["care_tasks"].items():
            print(f"     {task:<12}: every {info['every_days']} day(s), last done {info['last_done']}")
        print("  ╚══════════════════════════════════╝\n")

def log_care_task():
    print("\n  ✅ LOG CARE TASK")
    print("  " + "-" * 30)
    plant_id = input("  Enter Plant ID : ").strip()
    print("  Tasks: watering / fertilizing / pruning / pest_check")
    task     = input("  Which task done: ").strip().lower()
    today    = str(date.today())

    plants = load_plants()
    for p in plants:
        if p["id"] == plant_id:
            if task in p["care_tasks"]:
                p["care_tasks"][task]["last_done"] = today
                save_plants(plants)
                log_task(p["id"], p["name"], task, today)
                print(f"  ✅ {task} logged for {p['name']} on {today}!")
            else:
                print("  ❌ Invalid task name!")
            return
    print("  ❌ Plant ID not found!")

def delete_plant():
    print("\n  🗑️  DELETE PLANT")
    print("  " + "-" * 30)
    plant_id = input("  Enter Plant ID to delete: ").strip()
    plants   = load_plants()
    new_list = [p for p in plants if p["id"] != plant_id]
    if len(new_list) == len(plants):
        print("  ❌ Plant ID not found!")
    else:
        save_plants(new_list)
        print(f"  ✅ Plant {plant_id} deleted!")

def search_plant():
    print("\n  🔍 SEARCH PLANT")
    print("  " + "-" * 30)
    keyword = input("  Enter name, species or ID: ").strip().lower()
    plants  = load_plants()
    results = [p for p in plants if
               keyword in p["name"].lower() or
               keyword in p["species"].lower() or
               keyword in p["id"].lower()]
    if not results:
        print("  ❌ No plants found!")
        return
    print(f"\n  ✅ Found {len(results)} result(s):\n")
    for p in results:
        print(f"  🌿 [{p['id']}] {p['name']} — {p['species']}")

def plant_statistics():
    plants = load_plants()
    if not plants:
        print("  ⚠️  No plants registered yet.")
        return

    today = date.today()
    print("\n  📊 PLANT STATISTICS")
    print("  " + "=" * 40)
    print(f"  🌿 Total Plants : {len(plants)}")

    for p in plants:
        print(f"\n  [{p['id']}] {p['name']}")
        for task, info in p["care_tasks"].items():
            count = get_task_count(p["id"], task)
            last  = datetime.strptime(info["last_done"], "%Y-%m-%d").date()
            days_since = (today - last).days
            print(f"     {task:<12}: done {count} time(s), last {days_since} day(s) ago")
    print("  " + "=" * 40)
