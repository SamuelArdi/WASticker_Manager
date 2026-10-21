from backend import lib
import colors as wac

import flet as ft

# TODO: json implementation

def save_json():
  return

def load_json():
  return

# TODO: functionality to the add pack button

def on_add_pack():
  return

def main(page: ft.Page):
  page.title = "WASticker Manager"

  # add pack
  page.floating_action_button = ft.FloatingActionButton(
    icon=ft.Icons.ADD,
    foreground_color=wac.TEA_GREEN,
    bgcolor=wac.WA_LIGHT_GREEN
  )

  # topbar
  page.appbar = ft.AppBar(
    title=ft.Row(
      spacing=10,
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Icon(ft.Icons.STAR),
        ft.Text("WhatsApp Sticker Manager", color=wac.TEA_GREEN)
      ]
    ),
    leading=ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN),
    bgcolor=wac.WA_LIGHT_GREEN,
    actions=[
      ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
      ft.IconButton(ft.Icons.SETTINGS, icon_color=wac.TEA_GREEN)
    ]
  )

  # sticker packs
  # TODO: add the cards for the packs

if __name__ == "__main__":
  ft.run(main)
