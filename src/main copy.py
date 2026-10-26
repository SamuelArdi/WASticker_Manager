from backend import lib
import colors as wac

import flet as ft

# TODO: json implementation
packs: list[dict] = [{}]
def save_json():
  return

def load_json():
  return

class App_Main():
  def __init__(self, page: ft.Page):
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

  def pack_layout(pack: dict) -> ft.Control:
    return ft.Container(
      padding=10,
      border_radius=8,
      bgcolor=wac.LIGHT_NUDE,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[

          # icon
          ft.Container(), # currently placeholder

          # name and author
          ft.Column(
            controls=[
              ft.Text(packs["name"]),
              ft.Text(packs["author"]),
            ]
          ),
          ft.Button("Apply", data=pack)
        ]
      )
    )

def main(page: ft.Page):
  App_Main(page)

if __name__ == "__main__":
  ft.run(main)
