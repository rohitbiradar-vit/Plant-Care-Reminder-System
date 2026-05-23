from raf_handler import *
from file_handler import log_task, get_task_count
from datetime import date, datetime
from plant_data import get_plant_profile, PLANT_PROFILES


def add_plant():

    print("\n  🌱 ADD NEW PLANT")
    print("  " + "-" * 35)

    print("\n  🌿 Available Plant Profiles:")

    for key, value in PLANT_PROFILES.items():
        if key != "default":
            print(f"     → {value['common_name']} ({key})")

    print()

    # CHECK IF ID ALREADY EXISTS
    while True:

        plant_id = input("  Plant ID      : ").strip()

        plants = read_all_plants()

        found = False

        for p in plants:

            if p["id"].lower() == plant_id.lower():

                found = True
                break

        if found:

            print("\n  ❌ Plant ID already exists!")
            print("  🔁 Please enter another ID.\n")

        else:
            break
    name     = input("  Plant name    : ").strip()
    species  = input("  Species       : ").strip().lower()

    today = str(date.today())

    profile = get_plant_profile(species)

    print(f"\n  ✅ Profile Found : {profile['common_name']}")
    print(f"  💡 Tip           : {profile['tips']}")

    print("\n  📋 AUTO CARE SCHEDULE")

    for task, days in profile["care_tasks"].items():
        print(f"     → {task:<12}: every {days} day(s)")

    care_tasks = {
        task: {
            "every_days": days,
            "last_done": today
        }
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

    print(f"\n  ✅ {name} added successfully!")


def view_plants():

    plants = read_all_plants()

    if not plants:
        print("  ⚠️ No plants registered yet.")
        return

    print(f"\n  🪴 YOU HAVE {len(plants)} PLANT(S)\n")

    for p in plants:

        print("  ╔══════════════════════════════════╗")
        print(f"  🌿 ID      : {p['id']}")
        print(f"     Name    : {p['name']}")
        print(f"     Species : {p['species']}")

        for task, info in p["care_tasks"].items():

            print(f"     {task:<12}: every {info['every_days']} day(s)")

        print("  ╚══════════════════════════════════╝\n")


def log_care_task():

    print("\n  ✅ LOG CARE TASK")

    plant_id = input("  Enter Plant ID : ").strip()

    print("  Tasks: watering / fertilizing / pruning / pest_check / repotting")

    task = input("  Which task done: ").strip().lower()

    today = str(date.today())

    plant, slot = find_plant_by_id(plant_id)

    if not plant:
        print("  ❌ Plant ID not found!")
        return

    if task in plant["care_tasks"]:

        plant["care_tasks"][task]["last_done"] = today

        update_plant(slot, plant)

        log_task(plant["id"], plant["name"], task, today)

        print(f"  ✅ {task} logged for {plant['name']}!")

    else:
        print("  ❌ Invalid task!")


def delete_plant():

    print("\n  🗑️ DELETE PLANT")

    plant_id = input("  Enter Plant ID : ").strip()

    plant, slot = find_plant_by_id(plant_id)

    if not plant:
        print("  ❌ Plant not found!")
        return

    delete_plant_raf(slot)

    print(f"  ✅ Plant {plant_id} deleted!")


def search_plant():

    print("\n  🔍 SEARCH PLANT")

    plant_id = input("  Enter Plant ID : ").strip()

    plant, slot = find_plant_by_id(plant_id)

    if not plant:
        print("  ❌ Plant not found!")
        return

    print(f"\n  ✅ Plant Found at Slot {slot}")

    print(f"\n  🌿 ID      : {plant['id']}")
    print(f"     Name    : {plant['name']}")
    print(f"     Species : {plant['species']}")

    for task, info in plant["care_tasks"].items():

        print(f"     {task:<12}: every {info['every_days']} day(s)")


def plant_statistics():

    plants = read_all_plants()

    if not plants:
        print("  ⚠️ No plants registered yet.")
        return

    today = date.today()

    print("\n  📊 PLANT STATISTICS")
    print("  " + "=" * 40)

    print(f"  🌿 Total Plants : {len(plants)}")

    for p in plants:

        print(f"\n  [{p['id']}] {p['name']}")

        for task, info in p["care_tasks"].items():

            count = get_task_count(p["id"], task)

            last = datetime.strptime(
                info["last_done"],
                "%Y-%m-%d"
            ).date()

            days_since = (today - last).days

            print(
                f"     {task:<12}: done {count} time(s), "
                f"last {days_since} day(s) ago"
            )

    print("  " + "=" * 40)
