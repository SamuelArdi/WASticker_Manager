from backend import lib
import colors as wac

import flet as ft

def main(page: ft.Page):
  page.title = "WASticker Manager"

  page.floating_action_button = ft.FloatingActionButton(
    icon=ft.Icons.ADD,
  )

  # topbar
  page.appbar = ft.AppBar(
    title=ft.Text("WhatsApp Sticker Manager", color=wac.TEA_GREEN),
    center_title=True,
    leading=ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN),
    bgcolor=wac.WA_LIGHT_GREEN,
    actions=[
      ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
      ft.IconButton(ft.Icons.SETTINGS, icon_color=wac.TEA_GREEN)
    ]
  )

if __name__ == "__main__":
  ft.run(main)
