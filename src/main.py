from backend import lib
import colors as wac

import flet as ft

# GLOBALS
pack_list = ft.Column(
  spacing=10,
  horizontal_alignment=ft.CrossAxisAlignment.STRETCH
)

# TODO: json implementation
packs: list[dict] = [{}]
def save_json():
  return

def load_json():
  return

def refresh_list(page: ft.Page):
  pack_list.controls = [pack_layout(p) for p in packs]
  if not packs:
    pack_list.controls.append(
      ft.Text("No Packs yet. Tap + to add one.", color=ft.Colors.OUTLINE)
    )
  page.update()

def create_pack(packs: list[dict], page: ft.Page):
  packs.append(
    {"name": "DOMINION", "author": "CALL"},
  )
  refresh_list(page)

def pack_layout(pack_dict: dict) -> ft.Control:
  pack = ft.Container(
    padding=10,
    border_radius=8,
    bgcolor=wac.LIGHT_NUDE,
    content=ft.Row(
      spacing=3,
      controls=[

        # icon
        ft.Container(), # currently placeholder

        # name and author
        ft.Column(
          spacing=8,
          controls=[
            ft.Text("NAME"),
            ft.Text("AUTHOR")
          ]
        )
      ]
    )
  )

  return pack

def main(page: ft.Page):
  page.title = "WASticker Manager"

  # TODO: remove before prod
  page.window.width = 378
  page.window.height = 863
  page.window.resizable = False
  page.window.maximizable = False

  # add pack
  page.floating_action_button = ft.FloatingActionButton(
    icon=ft.Icons.ADD,
    foreground_color=wac.TEA_GREEN,
    bgcolor=wac.WA_LIGHT_GREEN,
    content="Create Pack",
    on_click=lambda c: create_pack(packs, page)
  )

  # topbar
  page.appbar = ft.AppBar(
    title=ft.Text("Sticker Packs", color=wac.TEA_GREEN),
    leading=ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN),
    bgcolor=wac.WA_LIGHT_GREEN,
    adaptive=True,
    actions=[
      ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
      ft.IconButton(ft.Icons.SETTINGS, icon_color=wac.TEA_GREEN)
    ]
  )

  page.add(pack_list)
  refresh_list(page)

if __name__ == "__main__":
  ft.run(main)
