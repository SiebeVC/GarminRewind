from datetime import datetime, timedelta
from collections import defaultdict, Counter


def make_rewind(df, name):
    with open("files/index.html", 'r') as temp:
        template = temp.read()

    session_count = len(df)
    template = template.replace("=SESSIONS=", str(session_count))

    # Total Days
    days = set()
    for i in range(session_count):
        d = datetime.strptime(df[(i, "Date")], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        days.add(d)
    template = template.replace("=DAYS=", str(len(days)))

    # Total Time
    time = []
    for i in range(session_count):
        d = datetime.strptime(df[(i, "Time")], "%H:%M:%S")
        delta = timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
        time.append(delta)

    total_time = sum(time, timedelta())
    seconds = total_time.total_seconds()
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    template = template.replace("=TIME=", f"{int(days)}d {int(hours)}h {int(minutes)}m")

    # Total Calories
    calories = sum([int(df[(i, "Calories")]) for i in range(session_count)])
    template = template.replace("=CALORIES=", str(calories))

    avg_heart = sum([int(df[(i, "Avg HR")]) for i in range(session_count)])
    template = template.replace("=AVGHEART=", str(round(avg_heart / session_count)))

    # Max Heart
    max_heart = max([int(df[(i, "Max HR")]) for i in range(session_count)])
    template = template.replace("=MAXHEART=", str(max_heart))

    # Max Height
    def reformat_height(s):
        s = s.replace('.', '')
        s = s.replace("--", '0')
        return int(s)

    max_height = max([reformat_height(df[(i, "Max Elevation")]) for i in range(session_count)])
    template = template.replace("=MAXHEIGHT=", str(max_height))

    # Total Height
    total_height = sum([reformat_height(df[(i, "Total Ascent")]) for i in range(session_count)])
    template = template.replace("=TOTALHEIGHT=", str(total_height))

    activities = []
    for i in range(session_count):
        activities.append(df[(i, "Activity Type")])
    counted = Counter(activities)

    c = 0
    for k, v in counted.items():
        c += 1
        template = template.replace(f"=ACT{c}=", f"{k} ({v})")

    while c < 5:
        c += 1
        template = template.replace(f"=ACT{c}=", "")

    template = template.replace("=NAME=", name)

    return str(template)
