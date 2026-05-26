LOG_FILE = "watering_log.txt"
REPORT_FILE = "report.txt"

def log_task(plant_id, plant_name, task, date):
    with open(LOG_FILE, "a") as f:
        f.write(f"{date} - [{plant_id}] {plant_name} — {task} done\n")

def view_log():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "  No history found."

def get_task_count(plant_id, task):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            return sum(1 for line in lines if plant_id in line and task in line)
    except FileNotFoundError:
        return 0

def save_report(content):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(content)