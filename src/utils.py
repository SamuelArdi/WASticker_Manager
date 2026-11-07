from datetime import datetime

WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

def _ensure_aware(dt: datetime) -> datetime:
  return dt.astimezone()

def format_date(
  then: datetime,
  now: datetime | None = None,
  *,
  weekday_cutoff: int = 6
)-> str:
  now = _ensure_aware(now or datetime.now())
  then = _ensure_aware(then)
  days = (now.date() - then.date()).days if now else (datetime.now().date() - then.date()).days

  if days < 0:
    return "Just Now"
  if days == 0:
    return f"{then.hour:02d}:{then.minute:02d}"
  if days == 1:
    return "Yesterday"
  if days <= weekday_cutoff:
    return WEEKDAY_NAMES[then.weekday()]
  if then.year == (now.year if now else datetime.now().year):
    return f"{MONTH_NAMES[then.month - 1]} {then.day}"
  return f"{MONTH_NAMES[then.month - 1]} {then.day}, {then.year}"
