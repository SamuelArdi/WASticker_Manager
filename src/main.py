from app import AppMain

import flet as ft
import locale

try:
  locale.setlocale(locale.LC_TIME, "") # set time to user's locale time
except locale.Error:
  pass

def main(page: ft.Page):
  #TODO: remove before prod
  import sys, os
  if sys.platform != "web" and not os.environ.get("FLET_DEV_MODE"):
    page.window.width = 378
    page.window.height = 863
    page.window.resizable = False
    page.window.maximizable = False
  AppMain(page)

if __name__ == "__main__":
  ft.run(main)
