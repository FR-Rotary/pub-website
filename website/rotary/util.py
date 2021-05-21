from datetime import datetime
def dict_from_row(row):
    return dict(zip(row.keys(), row))

def format_time(time):
    time = datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
    return time
