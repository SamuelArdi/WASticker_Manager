import flet as ft
import colors as wac

from views.base import BaseView

class EditView(BaseView):
  route = "/edit"

  def __init__(self, app):
    super().__init__(app)

    raw = self.page.query.get("pack_id")
    try:
      self.pack_id = int(raw) if raw is not None else None
    except (ValueError, TypeError):
      self.pack_id = None

    self.pack = next(
      (p for p in app.packs if p["id"] == self.pack_id), None
    ) if self.pack_id is not None else None

    self._pending_cover = self.pack.get("cover") if self.pack else None

  # ---------------------------------------------------- build 
  def build(self) -> ft.View:
    if self.pack is None:
      return self._build_not_found()

    name = ft.TextField(label="Pack Name", value=self.pack["name"], autofocus=True)
    author = ft.TextField(label="Author", value=self.pack["author"])
    cover_holder = ft.Container(
      width=96,
      height=96,
      border_radius=8,
      action=ft.PickFiles(
        self.app.file_picker,
        dialog_title="Choose cover image",
        file_type=ft.FilePickerFileType.IMAGE
      ),
      content=(
        ft.Image(
          src=self.pack["cover"],
          width=96,
          height=96,
          fit=ft.BoxFit.COVER,
          border_radius=8
        )
        if self.pack.get("cover")
        else ft.Icon(ft.Icons.ACCOUNT_BOX_ROUNDED, size=96)
      )
    )

    def handle_result(e: ft.FilePickerResultEvent):
      if e.files and e.files[0].path:
        self._pending_cover = e.files[0].path
        cover_holder.content = ft.Image(
          src=self._pending_cover,
          width=96, height=96,
          fit=ft.BoxFit.COVER,
          border_radius=8,
        )
        cover_holder.update()
    
    self.app.file_picker.on_result = handle_result

    # ---------------------------------------------------- actions
    def save(e=None):
      if self.pack is None:
        self.page.navigate("/")
        return
      if not (name.value or "").strip():
        name.error = ft.Text("Pack name is required")
        name.update()
        return

      self.pack["name"] = name.value.strip()
      self.pack["author"] = author.value.strip() or "Unknown"
      self.pack["cover"] = self._pending_cover

      self.page.navigate("/")

    def confirm_delete(e=None):
      self.app.packs.remove(self.pack)
      self.page.pop_dialog()
      #TODO: save_packs()
      self.page.navigate("/")

    def delete(e=None):
      assert self.pack is not None

      self.page.show_dialog(
        ft.AlertDialog(
          modal=True,
          title=ft.Text("Delete Pack?"),
          content=ft.Text(f"{self.pack.get('name')} will be permanently removed."),
          actions=[
            ft.TextButton(
              "Cancel",
              on_click=lambda _: self.page.pop_dialog()
            ),
            ft.FilledButton(
              "Delete",
              bgcolor=ft.Colors.RED_600,
              color=ft.Colors.WHITE,
              on_click=confirm_delete
            )
          ]
        )
      )
    # ---------------------------------------------------- view 
    return ft.View(
      route=self.route,
      appbar=self.build_appbar(
        "Edit Pack", back=True,
        actions=[
          ft.IconButton(
            ft.Icons.CHECK, icon_color=wac.TEA_GREEN,
            tooltip="Save", on_click=save
          )
        ]
      ),
      controls=[
        ft.SafeArea(
          ft.Column(
            [
              ft.Container(height=8),
              ft.Row(
                [cover_holder],
                alignment=ft.MainAxisAlignment.CENTER
              ),
              ft.Container(height=16),
              name,
              author,
              ft.Container(height=24),
              ft.TextButton(
                "Delete pack",
                icon=ft.Icons.DELETE_OUTLINE,
                style=ft.ButtonStyle(color=ft.Colors.RED_600),
                on_click=delete
              )
            ],
            tight=True,
            spacing=12
          ),
          expand=True
        )
      ]
    )

  # ---------------------------------------------------- fallback
  def _build_not_found(self) -> ft.View:
    return ft.View(
      route=self.route,
      appbar=self.build_appbar("Edit Pack", back=True),
      controls=[
        ft.SafeArea(
          ft.Column([
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=48),
            ft.Text("Pack not found", size=16),
            ft.Button("Back to home", on_click=lambda _: self.page.navigate("/")),
          ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
          expand=True
        )
      ]
    )
