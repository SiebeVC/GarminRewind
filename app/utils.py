from datetime import datetime

def try_parse_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', "%d-%m-%y %H:%M"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found: ', date_str)

def reformat(s):
    s = s.replace('.', '')
    s = s.replace(',', '')
    s = s.replace("--", '0')
    return int(s)