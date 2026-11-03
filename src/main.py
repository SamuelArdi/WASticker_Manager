from app import AppMain

import flet as ft
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "") # set time to user's locale time


def main(page: ft.Page):
  #TODO: remove before prod
  page.window.width = 378
  page.window.height = 863
  page.window.resizable = False
  page.window.maximizable = False
  AppMain(page)

if __name__ == "__main__":
  ft.run(main)
