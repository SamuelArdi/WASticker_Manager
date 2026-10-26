from backend import lib
import colors as wac

import flet as ft

# TODO: json implementation
packs: list[dict] = []
def save_packs():
  return

def load_packs():
  return

class AppMain():

  def __init__(self, page: ft.Page):
    self.page = page
    self.pack_column = ft.Column(
      spacing=12,
      horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    # TODO: remove before prod
    self.page.window.width = 378
    self.page.window.height = 863
    self.page.window.resizable = False
    self.page.window.maximizable = False

    # add pack
    self.page.floating_action_button = ft.FloatingActionButton(
      icon=ft.Icons.ADD,
      foreground_color=wac.TEA_GREEN,
      bgcolor=wac.WA_LIGHT_GREEN,
      content="Create Pack",
      on_click=lambda c: self.create_pack()
    )

    self. page.appbar = ft.AppBar(
      title=ft.Text("Sticker Packs", color=wac.TEA_GREEN),
      leading=ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN),
      bgcolor=wac.WA_LIGHT_GREEN,
      adaptive=True,
      actions=[
        ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
        ft.IconButton(ft.Icons.SETTINGS, icon_color=wac.TEA_GREEN)
      ]
    )

    self.page.add(self.pack_column)
    self._rebuild()

  # ----------------------------------------------------
  def _layout(self, pack: dict) -> ft.Control:
    #TODO: add a apply button on the right of the card
    return ft.Container(
      padding=10,
      border_radius=8,
      bgcolor=wac.LIGHT_NUDE,
      content=ft.Row(
        controls=[

          # icon
          ft.Container(), # currently placeholder

          # name and author
          ft.Column(
            controls=[
              ft.Text(pack["name"]),
              ft.Text(pack["author"]),
            ]
          ),
        ]
      )
    )

  def _rebuild(self):
    self.pack_column.controls = (
      [self._layout(p) for p in packs]
      if packs
      else [ft.Text("No packs yet, create a pack by pressing the + button.")]
    )
    self.page.update()

  # ----------------------------------------------------
  def create_pack(self, e: ft.Event[ft.Button] | None = None):
    packs.append(
      {"name": "COURTESY", "author": "CALL", "date": "Thousand Foot Krutch"}
    )
    self._rebuild()

def main(page: ft.Page):
  AppMain(page)

if __name__ == "__main__":
  ft.run(main)
