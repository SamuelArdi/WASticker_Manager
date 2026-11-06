import colors as wac
from native_loader import lib
if lib is None:
  print("Running without native backend")

from views import HomeView, SettingsView, EditView

import flet as ft
from datetime import datetime
from urllib.parse import urlparse

class AppMain():
  def __init__(self, page: ft.Page):
    self.page = page

    #TODO: replace with load_packs()
    # self.packs: list[dict] = [
    #   {
    #     "id": 0,
    #     "cover": None,
    #     "name": "TEST PACK",
    #     "author": "Unknown",
    #     "date": datetime.today()
    #   }
    # ]
    self.packs: list[dict] = []

    # file picker service
    self.file_picker = ft.FilePicker()
    self.page.services.append(self.file_picker)

    self.routes = {
      "/": HomeView,
      "/settings": SettingsView,
      "/edit": EditView
    }
    self.current_view = None

    self.page.on_route_change = self.route_change 
    self.page.on_view_pop = self.view_pop

    self.route_change()

  # ---------------------------------------------------- dialog: create pack
  #TODO: improve the layout of the dialog
  def create_pack(self, e: ft.Event[ft.Button] | None = None):
    name = ft.TextField(label="Pack name", autofocus=True)
    author = ft.TextField(label="Author")
    cover: list[str] = []
    cover_holder = ft.Container(action=ft.PickFiles(
      self.file_picker,
      dialog_title="Choose cover image",
      file_type=ft.FilePickerFileType.IMAGE
    ), width=96, height=96, content=ft.Icon(ft.Icons.ACCOUNT_BOX_ROUNDED, size=96))

    def handle_result(e: ft.FilePickerResultEvent):
      if e.files and e.files[0].path:
        cover.clear()
        cover.append(e.files[0].path)
        cover_holder.content = ft.Image(
          src=e.files[0].path, width=96, height=96,
          fit=ft.BoxFit.COVER, border_radius=8,
        )
        cover_holder.update()

    self.file_picker.on_result = handle_result

    def confirm(e):
      if not (name.value or "").strip():
        name.error = ft.Text("Pack name is required")
        name.update()
        return

      self.packs.append({
        "id": max((p["id"] for p in self.packs), default=-1) + 1,
        "cover": cover[0] if cover else None,
        "name": name.value.strip(),
        "author": author.value.strip() or "Unknown",
        "date": datetime.today()
      })

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
      # actions_padding=15,
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

  # ---------------------------------------------------- routing
  def route_change(self, e: ft.RouteChangeEvent | None = None):
    self.page.views.clear()

    path = urlparse(self.page.route).path or "/"
    view_cls = self.routes.get(path, HomeView)
    print(f"[route] matched {view_cls.__name__} for {path!r}")

    self.current_view = view_cls(self)
    self.page.views.append(self.current_view.build())
    self.page.update()

  async def view_pop(self, e: ft.ViewPopEvent):
    if e.view is not None and e.view in self.page.views:
      self.page.views.remove(e.view)
    if self.page.views:
      await self.page.push_route(self.page.views[-1].route)
    
  def edit_pack(self, pack):
    return
