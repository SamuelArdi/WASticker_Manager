from backend import lib
import colors as wac

import flet as ft

# TODO: save and load implementation
packs: list[dict] = []
def save_packs():
  return

def load_packs():
  return

class AppMain():
  def __init__(self, page: ft.Page):
    self.page = page

    # add file picker service into the app
    self.file_picker = ft.FilePicker()
    self.page.services.append(self.file_picker)

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
      on_click=self.create_pack
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

    self.pack_column = ft.Column(
      spacing=12,
      horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
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
          (
            ft.Image(src=pack["cover"], width=48, height=48, fit=ft.BoxFit.COVER, border_radius=8)
            if pack.get("cover")
            else ft.Icon(ft.Icons.IMAGE)
          ),

          # name and author
          ft.Column(
            controls=[
              ft.Text(pack["name"]),
              ft.Text(pack["author"]),
            ]
          )
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
  async def create_pack(self, e: ft.Event[ft.Button] | None = None):
    #TODO: fix "cover image" button sometimes not working

    name = ft.TextField(label="Pack name", autofocus=True)
    author = ft.TextField(label="Author")
    cover: list[str] = []
    cover_holder = ft.Container(height=96, visible=False)

    def handle_result(e: ft.FilePickerResultEvent):
      if e.files and e.files[0].path:
        cover.clear()
        cover.append(e.files[0].path)
        cover_holder.content = ft.Image(
          src=e.files[0].path, width=96, height=96,
          fit=ft.BoxFit.COVER, border_radius=8,
        )
        cover_holder.visible = True
        cover_holder.update()

    self.file_picker.on_result = handle_result

    async def confirm(e):
      if not (name.value or "").strip():
        name.error = ft.Text("Pack name is required")
        name.update()
        return

      packs.append({"name": name.value.strip(), "author": author.value.strip() or "Unknown", "cover": cover[0] if cover else None})
      self.page.pop_dialog()
      self._rebuild()

    self.page.show_dialog(ft.AlertDialog(
      modal=True,
      title=ft.Text("Create Sticker Pack"),
      content=ft.Column([
        cover_holder,
        ft.FilledTonalButton(
          "Choose Cover",
          action=ft.PickFiles(
            self.file_picker,
            dialog_title="Choose cover image",
            file_type=ft.FilePickerFileType.IMAGE
          )
        ),
        name, author
      ], tight=True),
      actions=[
        ft.TextButton("Cancel", on_click=lambda e: self.page.pop_dialog()),
        ft.FilledButton("Create", on_click=confirm)
      ]
    ))

def main(page: ft.Page):
  AppMain(page)

if __name__ == "__main__":
  ft.run(main)
