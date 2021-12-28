# inspired by:
# https://forum.roamresearch.com/t/how-i-quickly-navigate-in-time/610

import os
from datetime import datetime
from datetime import timedelta
from itertools import cycle

def get_first_day(year):
    return datetime(year, 1, 1)


def get_months(year):
    return [datetime(year, i, 1) for i in range(1, 13)]


def format_months(months):
    months_text = [f"[{d.strftime('%b %y')}]([[{d.strftime('%B %Y')}]])" for d in months]
    return ' || '.join(months_text)


def get_weeks(month):
    d = datetime(month.year, month.month, month.day)
    weeks = []
    while d.month == month.month:
        weeks.append(d)
        while True:
            d += timedelta(days=1)
            if d.weekday() == 0:
                break
    return weeks

def format_weeks(weeks):
    weeks_text = [f"[W{d.strftime('%W')}]([[{d.strftime('%YW%W')}]])" for d in weeks]
    return " || ".join(weeks_text)


def get_days_of_month(month):
    d = datetime(month.year, month.month, month.day)
    days = []
    while d.month == month.month:
        days.append(d)
        d += timedelta(days=1)
    return days


def get_days_of_week(week):
    days = []
    d = datetime(week.year, week.month, week.day)
    while True:
        days.append(d)
        d += timedelta(days=1)
        if d.weekday() == 0:
            break
    return days
        

def format_day(d, alias):
    day_number = f"{d.day}"
    if d.day != 11 and d.day % 10 == 1:
        day_number += "st"
    elif d.day != 12 and d.day % 10 == 2:
        day_number += "nd"
    elif d.day != 13 and d.day % 10 == 3:
        day_number += "rd"
    else:
        day_number += "th"

    return f"[{alias}]([[{d.strftime('%B')} {day_number}, {d.strftime('%Y')}]])"

def format_calendar(days):
    cols = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    head = ""
    for i, name in enumerate(cols):
        head += "\t" * i + f"- {name}\n"

    body = ""
    idx = 0
    for i, col in enumerate(cycle(cols)):
        if idx == len(days):
            break
        if days[idx].strftime("%a") != col:
            text = ""
        else:
            text = format_day(days[idx], alias=days[idx].day)
            idx += 1
        padding = "\t" * (i % len(cols))
        body += padding + f"- {text}\n"

    return head + body


def format_days_of_week(days):
    return " || ".join(format_day(d, alias=d.strftime("%a %d")) for d in days)


def get_year_page(year):
    title = f"{year}"
    months = get_months(year)
    return title, format_months(months)


def get_month_page(month):
    weeks = get_weeks(m)

    days = get_days_of_month(m)
    calendar = format_calendar(days)

    table = "{{[[table]]}}\n"
    table += "\n".join([f"\t{row}" for row in calendar.split("\n")])

    title = month.strftime("%B %Y")
    return title, "\n".join([format_weeks(weeks), table])


def get_week_page(week):
    days = get_days_of_week(w)
    title = week.strftime('%YW%W')
    return title, format_days_of_week(days)


def write_file(outdir, title, content, ext="md"):
    outpath = os.path.join(outdir, f"{title}.{ext}")
    with open(outpath, "w") as fp:
        fp.write(content)
        # fp.write("\n".join([f"\t{row}" for row in content.split("\n")]))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Roam templates for yearly time management")
    parser.add_argument('year', type=int, help='Year number')
    parser.add_argument('outdir', help='Dir to write output files to')

    args = parser.parse_args()

    # write year file
    write_file(args.outdir, *get_year_page(args.year))

    months = get_months(args.year)
    for m in months:
        # write month file
        write_file(args.outdir, *get_month_page(m))

        weeks = get_weeks(m)
        for w in weeks:
            # write week page
            write_file(args.outdir, *get_week_page(w))




