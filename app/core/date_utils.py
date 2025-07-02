from datetime import datetime, timedelta
from dateparser.search import search_dates
import re

def infer_dates(time_expression: str, original_query: str = ""):
    now = datetime.today()
    expression = (time_expression or original_query).lower().strip()

    expression = expression.replace("the last", "last").replace("the past", "past")

    match = re.search(r"(last|past|previous)\s+(\d+)?\s*(day|days|month|months|year|years)", expression)
    if match:
        quantity = int(match.group(2)) if match.group(2) else 1
        unit = match.group(3)

        if "day" in unit:
            delta = timedelta(days=quantity)
        elif "month" in unit:
            delta = timedelta(days=30 * quantity)
        elif "year" in unit:
            delta = timedelta(days=365 * quantity)
        else:
            delta = timedelta(days=0)

        end = now
        start = now - delta
        return start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y")

    parsed = search_dates(expression, settings={"RELATIVE_BASE": now})
    if parsed:
        dates = sorted(set([d[1] for d in parsed if isinstance(d[1], datetime)]))
        if len(dates) == 1:
            return dates[0].strftime("%d-%m-%Y"), "not mentioned"
        elif len(dates) >= 2:
            return dates[0].strftime("%d-%m-%Y"), dates[-1].strftime("%d-%m-%Y")

    return "not mentioned", "not mentioned"
