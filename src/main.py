from backend import lib
import colors as wac

import flet as ft
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "") # set time to user's locale time

#NOTE: todo tomorrow:
# - add apply button
# - add new screen to edit the packs

# TODO: save and load implementation
# NOTE: possibly do this in C++ so it gets executed faster
packs: list[dict] = []
def save_packs():
  return

def load_packs():
  return

class FormatDate:
  WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednedsay", "Thursday", "Friday", "Saturday", "Saturday", "Sunday")
  MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

  def __init__(self, then: datetime, now: datetime | None = None, *, weekday_cutoff: int = 6) -> None:
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

    # add pack button
    self.page.floating_action_button = ft.FloatingActionButton(
      icon=ft.Icons.ADD,
      foreground_color=wac.TEA_GREEN,
      bgcolor=wac.WA_LIGHT_GREEN,
      content=ft.Text("Create Pack"),
      on_click=self.create_pack
    )

    # topbar
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
      content=ft.Row([
        ft.Row([
          # icon
          (
            ft.Image(src=pack["cover"], width=48, height=48, fit=ft.BoxFit.COVER, border_radius=8)
            if pack.get("cover")
            else ft.Icon(ft.Icons.IMAGE, size=48)
          ),
          # name and author
          ft.Column([
            ft.Text(pack["name"]),
            ft.Text(pack["author"], size=12, opacity=0.6),
            ft.Text("")
          ], tight=True, spacing=0),
        ]),
        ft.Column([
          # pack actions
          ft.Row([
            ft.IconButton(ft.Icons.EDIT),
            ft.IconButton(ft.Icons.MENU),
          ]),

          # date
          ft.Text(FormatDate(pack["date"]).label()),
        ]),
      ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
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

      packs.append({
        "cover": cover[0] if cover else None,
        "name": name.value.strip(),
        "author": author.value.strip() or "Unknown",
        "date": datetime.today()
      })
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
