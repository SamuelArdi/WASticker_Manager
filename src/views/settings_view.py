import flet as ft

from views.base import BaseView

class SettingsView(BaseView):
  route = "/settings"

  def build(self) -> ft.View:
    return ft.View(
      route=self.route,
      appbar=self.build_appbar("Settings", back=True),
      controls=[
        ft.SafeArea(
          ft.Column([
            ft.Switch(label="Dark mode", value=False),
            ft.Switch(label="Notifications", value=True),
            ft.Switch(label="Auto-save packs", value=True),
            ft.Divider(),
            ft.ListTile(
              leading=ft.Icon(ft.Icons.INFO_OUTLINE),
              title=ft.Text("About"),
              subtitle=ft.Text("Sticker Packs v0.1.0")
            )
          ], spacing=4, expand=True),expand=True
        )
      ]
    )
