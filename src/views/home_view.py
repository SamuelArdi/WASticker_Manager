import flet as ft
import colors as wac

from views.base import BaseView
from utils import FormatDate

class HomeView(BaseView):
  route = "/"

  def __init__(self, app):
    super().__init__(app)
    self.pack_column = ft.Column(
      spacing=12,
      horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
      scroll=ft.ScrollMode.AUTO,
      expand=True
    )
    self.rebuild()
  
  def _layout(self, pack: dict) -> ft.Control:
    #TODO: improve the positioning of the cards  
    return ft.Container(
      padding=8,
      border_radius=8,
      bgcolor=wac.LIGHT_NUDE,
      alignment=ft.Alignment.TOP_LEFT,
      content=ft.Row([
        ft.Row([
          # icon
          ft.Image(src=pack["cover"], width=72, height=72, fit=ft.BoxFit.COVER, border_radius=8)
          if pack.get("cover")
          else ft.Icon(ft.Icons.IMAGE, size=72),

          # name and author
          ft.Column([
            ft.Text(pack["name"], size=16),
            ft.Text(pack["author"], size=12, opacity=0.6),
            ft.Container(height=12),
          ], tight=True, spacing=0),
        ], spacing=10),

        ft.Column([
          ft.Row([
            # pack actions
            ft.IconButton(ft.Icons.EDIT, on_click=lambda _, p=pack: self.page.navigate("/edit", pack_id=str(p["id"]))),
            ft.ContextMenu(ft.IconButton(
              icon=ft.Icons.MORE_VERT,
              key="context_menu_trigger_area",
              expand=True,
            ), primary_items=[
              #TODO: enable after building the feature
              ft.PopupMenuItem("Apply", disabled=True),
              ft.PopupMenuItem(ft.Text("Delete", color=ft.Colors.RED), disabled=True),
            ], primary_trigger=ft.ContextMenuTrigger.DOWN)
          ], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.START),

          # date
          ft.Text(FormatDate(pack["date"]).label()),
        ], horizontal_alignment=ft.CrossAxisAlignment.END)
      ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START)
    )

  def rebuild(self):
    packs = self.app.packs
    self.pack_column.controls = (
      [self._layout(p) for p in packs]
      if packs
      else [ft.Text("No packs yet, create a pack by pressing the + button.")]
    )

  def build(self) -> ft.View:
    return ft.View(
      route=self.route,
      appbar=self.build_appbar("Sticker Packs"),
      controls=[ft.SafeArea(self.pack_column, expand=True)],
      floating_action_button=ft.FloatingActionButton(
        icon=ft.Icon(ft.Icons.ADD),
        foreground_color=wac.TEA_GREEN,
        bgcolor=wac.WA_LIGHT_GREEN,
        content=ft.Text("Create Pack"),
        on_click=self.app.create_pack
      ),
      floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT
    )
