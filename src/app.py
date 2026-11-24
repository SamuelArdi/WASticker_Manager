import sys
from datetime import datetime
from urllib.parse import urlparse

import flet as ft

from colors import Terminal as ttc
from native_loader import lib
from views import EditView, HomeView, SettingsView

if lib is None:
  print(f"{ttc.RED}Failed to find native backend (native.dll).{ttc.RESET}")
  sys.exit() # system exits as native.dll is a core component

class AppMain:

  MAX_PACKS: int = 25
  MAX_STICKERS: int = 30

  total_packs: int = 0
  total_stickers: int = 0

  def __init__(self, page: ft.Page):
    self.page = page

    #TODO: load_packs()

    self.packs: list[dict] = []
    self.routes = {
      "/": HomeView,
      "/settings": SettingsView,
      "/edit": EditView
    }

    # file picker service
    self.file_picker = ft.FilePicker()
    self.page.services.append(self.file_picker)
    self.current_view = None

    self.page.on_route_change = self.route_change

    self.route_change()

  # ---------------------------------------------------- dialog: create pack
  def create_pack(self, e: ft.Event[ft.Button] | None = None):
    if self.total_packs >= self.MAX_PACKS:
      self.page.show_dialog(ft.SnackBar(ft.Text("You've reached the maximum amount of packs available.")))
      return

    name = ft.TextField(label="Pack name", autofocus=True)
    author = ft.TextField(label="Author")
    cover_path: str | None = None
    cover_holder = ft.Row([
      ft.Container(action=ft.PickFiles(
        self.file_picker,
        dialog_title="Choose cover image",
        file_type=ft.FilePickerFileType.IMAGE
      ), width=96, height=96, content=ft.Icon(ft.Icons.IMAGE, size=96), padding=0)
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def _on_cover_picked(path: str):
      nonlocal cover_path
      cover_path = path
      cover_holder.controls[0] = ft.Image(
        src=path,
        width=96, height=96,
        fit=ft.BoxFit.COVER,
        border_radius=8
      )
      if cover_holder.page:
        cover_holder.update()
    self.pick_image(_on_cover_picked)

    def confirm(e):
      if not (name.value or "").strip():
        name.error = "Pack name is required"
        name.update()
        return

      if len(name.value) < 3:
        name.error = "Pack name cannot be shorter than 3"
        name.update()
        return

      self.packs.append({
        "id": self.total_packs,
        "cover": cover_path,
        "name": name.value.strip(),
        "author": author.value.strip() or "Unknown",
        "date": datetime.now()
      })
      self.total_packs += 1

      #TODO: add save_packs()

      self.page.pop_dialog()
      if self.current_view is not None:
        self.current_view.rebuild()
      self.page.update()

    self.page.show_dialog(ft.AlertDialog(
      modal=True,
      title=ft.Text("Create Sticker Pack"),
      content_padding=15,
      title_padding=15,
      content=ft.Column([
        cover_holder,
        ft.Container(height=15),
        name,
        author
      ], tight=True),
      actions=[
        ft.TextButton("Cancel", on_click=lambda e: self.page.pop_dialog()),
        ft.FilledButton("Create", on_click=confirm)
      ],
    ))

  def pick_image(self, on_picked):
    def _handle(e: ft.FilePickerResultEvent):
      if e.files and e.files[0].path:
        on_picked(e.files[0].path)
    self.file_picker.on_result = _handle

  # ---------------------------------------------------- routing
  def route_change(self, e: ft.RouteChangeEvent | None = None):
    self.page.views.clear()

    path = urlparse(self.page.route).path or "/"
    view_cls = self.routes.get(path, HomeView)

    self.current_view = view_cls(self)
    self.page.views.append(self.current_view.build())
    self.page.update()

  def edit_pack(self, pack):
    return
