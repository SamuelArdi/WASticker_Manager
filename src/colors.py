from enum import StrEnum


class WhatsApp:
  WA_TEAL_GREEN = "#215C54"
  WINTERGREEN_DREAM = "#35897E"
  WA_LIGHT_GREEN = "#59CE72"
  TEA_GREEN = "#E0F6CA"
  WA_CHECKMARK_BLUE = "#4FB6EC"
  LIGHT_NUDE = "#EBE5DE"

class Terminal(StrEnum):
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  BOLD = "\033[1m"
  RESET = "\033[0m"
