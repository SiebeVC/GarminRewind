from datetime import datetime, timedelta
from collections import Counter
from app.utils import try_parse_date, reformat


def make_rewind(df, name):
    with open("files/index.html", 'r') as temp:
        template = temp.read()

    session_count = len(df)
    template = template.replace("=SESSIONS=", str(session_count))

    # Total Days
    days = set()
    for i in range(session_count):
        try:
            d = try_parse_date(df[(i, "Date")]).strftime("%Y-%m-%d")
            days.add(d)
        except Exception as e:
            print(e)
    template = template.replace("=DAYS=", str(len(days)))

    # Total Time
    time = []
    for i in range(session_count):
        fmt = "%H:%M:%S"
        try:
            try:
                d = datetime.strptime(df[(i, "Time")], fmt)
            except ValueError as v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    line = df[(i, "Time")][:-(len(v.args[0]) - 26)]
                    d = datetime.strptime(line, fmt)
                else:
                    raise
            delta = timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
            time.append(delta)
        except Exception as e:
            print("Error: ", e)
            pass

    total_time = sum(time, timedelta())
    seconds = total_time.total_seconds()
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    template = template.replace("=TIME=", f"{int(days)}d {int(hours)}h {int(minutes)}m")

    # Total Calories
    calories = sum([reformat(df[(i, "Calories")]) for i in range(session_count)])
    template = template.replace("=CALORIES=", str(calories))

    avg_heart = sum([reformat(df[(i, "Avg HR")]) for i in range(session_count)])
    template = template.replace("=AVGHEART=", str(round(avg_heart / session_count)))

    # Max Heart
    max_heart = max([reformat(df[(i, "Max HR")]) for i in range(session_count)])
    template = template.replace("=MAXHEART=", str(max_heart))

    # Max Height
    max_height = max([reformat(df[(i, "Max Elevation")]) for i in range(session_count)])
    template = template.replace("=MAXHEIGHT=", str(max_height))

    # Total Height
    total_height = sum([reformat(df[(i, "Total Ascent")]) for i in range(session_count)])
    template = template.replace("=TOTALHEIGHT=", str(total_height))

    activities = []
    for i in range(session_count):
        activities.append(df[(i, "Activity Type")])
    counted = Counter(activities)

    #order counted
    ordered = {}
    for i in counted:
        ordered[i] = counted[i]

    ordered = dict(sorted(ordered.items(), key=lambda item: item[1], reverse=True))

    c = 0
    for k, v in ordered.items():
        c += 1
        template = template.replace(f"=ACT{c}=", f"{k} ({v})")

    while c < 5:
        c += 1
        template = template.replace(f"=ACT{c}=", "")

    template = template.replace("=NAME=", name)

    return str(template)
