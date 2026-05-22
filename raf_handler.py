import json

RAF_FILE = "plants_raf.txt"
SLOT_SIZE = 1000


def write_plant(slot, plant):

    record = json.dumps(plant)

    # fixed size record
    record = record.ljust(SLOT_SIZE)

    with open(RAF_FILE, "a+") as f:
        f.seek(slot * SLOT_SIZE)
        f.write(record)


def read_all_plants():

    plants = []

    try:
        with open(RAF_FILE, "r") as f:

            while True:

                record = f.read(SLOT_SIZE)

                if not record:
                    break

                record = record.strip()

                if record:
                    plants.append(json.loads(record))

    except FileNotFoundError:
        return []

    return plants


def get_total_slots():

    try:
        with open(RAF_FILE, "r") as f:

            f.seek(0, 2)

            return f.tell() // SLOT_SIZE

    except FileNotFoundError:
        return 0


def find_plant_by_id(plant_id):

    try:
        with open(RAF_FILE, "r") as f:

            slot = 0

            while True:

                record = f.read(SLOT_SIZE)

                if not record:
                    break

                record = record.strip()

                if record:

                    plant = json.loads(record)

                    if plant["id"] == plant_id:
                        return plant, slot

                slot += 1

    except FileNotFoundError:
        return None, -1

    return None, -1


def update_plant(slot, plant):

    record = json.dumps(plant).ljust(SLOT_SIZE)

    with open(RAF_FILE, "r+") as f:

        f.seek(slot * SLOT_SIZE)

        f.write(record)


def delete_plant_raf(slot):

    with open(RAF_FILE, "r+") as f:

        f.seek(slot * SLOT_SIZE)

        f.write(" " * SLOT_SIZE)