import flet as ft
import colors as wac

class BaseView:
  route: str = "/"

  def __init__(self, app):
    self.app = app
    self.page = app.page

  # ---------------------------------------------------- page
  def build_appbar(self, title: str, *, back: bool = False, actions: list[ft.Control] | None = None) -> ft.AppBar:
    if back:
      leading = ft.IconButton(
        ft.Icons.ARROW_BACK,
        icon_color=wac.TEA_GREEN,
        on_click=lambda _: self.page.navigate("/")
      )
      default_actions: list[ft.Control] = []
    else:
      leading = ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN)
      default_actions = [
        ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
        ft.IconButton(
          ft.Icons.SETTINGS,
          icon_color=wac.TEA_GREEN,
          on_click=lambda _: self.page.navigate("/settings")
        )
      ]

    return ft.AppBar(
      title=ft.Text(title, color=wac.TEA_GREEN),
      leading=leading,
      bgcolor=wac.WA_LIGHT_GREEN,
      adaptive=True,
      actions=actions if actions is not None else default_actions
    )
  
  def build(self) -> ft.View:
    raise NotImplementedError
  
  def rebuild(self) -> None:
    pass
