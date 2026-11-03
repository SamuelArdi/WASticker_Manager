from datetime import datetime

class FormatDate:
  WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
  MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

  def __init__(self,
               then: datetime,
               now: datetime | None = None,
               *,
               weekday_cutoff: int = 6
  ) -> None:
    self.now = self._local_aware(now or datetime.now())
    self.then = self._local_aware(then)
    self.days = (self.now.date() - self.then.date()).days
    self.weekday_cutoff = weekday_cutoff

  def label(self) -> str:
    if self.days < 0:
      return "Just Now"
    if self.days == 0:
      return self._format_time(self.then)
    if self.days == 1:
      return "Yesterday"
    if self.days <= self.weekday_cutoff:
      return self.WEEKDAY_NAMES[self.then.weekday()]
    if self.then.year == self.now.year:
      return f"{self.MONTH_NAMES[self.then.month - 1]} {self.then.day}"
    return f"{self.MONTH_NAMES[self.then.month - 1]} {self.then.day}, {self.then.year}"

  def _local_aware(self, dt: datetime) -> datetime:
    return dt.astimezone()

  def _format_time(self, dt: datetime) -> str:
    return f"{dt.hour:02d}:{dt.minute:02d}"
