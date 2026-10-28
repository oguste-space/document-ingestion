"""Legacy, best-effort date parser. Deprecated for compliance workflows."""
from datetime import date, datetime

def guess_date(text: str) -> date | None:
    for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(text.strip(), pattern).date()
        except ValueError:
            continue
    return None
