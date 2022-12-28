import pandas as pd


def make_rewind(df, name):
    with open("../files/index.html", 'r') as temp:
        template = temp.read()

    session_count = len(df)
    template = template.replace("=SESSIONS=", str(session_count))

    df['Date'] = pd.to_datetime(df['Date'])
    df['ShortDate'] = df['Date'].dt.strftime('%Y-%m-%d')
    day_count = len(df['ShortDate'].unique())
    template = template.replace("=DAYS=", str(day_count))

    df['Time'] = pd.to_timedelta(df['Time'])
    total_time = df['Time'].sum()
    seconds = total_time.total_seconds()
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    template = template.replace("=TIME=", f"{int(days)}d {int(hours)}h {int(minutes)}m")

    calories = round(df['Calories'].sum())
    template = template.replace("=CALORIES=", str(calories))

    average_heart_rate = round(df['Avg HR'].mean())
    template = template.replace("=AVGHEART=", str(average_heart_rate))

    max_heart_rate = round(df['Max HR'].max())
    template = template.replace("=MAXHEART=", str(max_heart_rate))

    def reformat_height(s):
        s = s.replace('.', '')
        s = s.replace("--", '0')
        return float(s)

    df["Max Height"] = df["Max Elevation"].apply(reformat_height).astype(float)
    highest_point = round(df['Max Height'].max())
    template = template.replace("=MAXHEIGHT=", str(highest_point))

    total_height = round(df['Total Ascent'].apply(reformat_height).astype(float).sum())
    template = template.replace("=TOTALHEIGHT=", str(total_height))

    activity_types = {**df['Activity Type'].value_counts()}
    i = 1
    for k, v in activity_types.items():
        if i > 4:
            break
        template = template.replace(f"=ACT{i}=", str(k) + " - " + str(v))
        i += 1

    while i <= 4:
        template = template.replace(f"=ACT{i}=", "")
        i += 1

    template = template.replace("=NAME=", name)

    return str(template)
