import flet as ft

from colors import Terminal as ttc
from colors import WhatsApp as wac
from views.base import BaseView


class EditView(BaseView):
  route = "/edit"

  def __init__(self, app):
    super().__init__(app)
    raw = self.page.query.to_dict.get("pack_id")

    try:
      self.pack_id = int(raw) if raw is not None else None
    except (ValueError, TypeError):
      self.pack_id = None

    self.pack: dict | None = next(
      (p for p in app.packs if p["id"] == self.pack_id), None
    ) if self.pack_id is not None else None

    self._pending_cover = self.pack.get("cover") if self.pack else None

    self.stickers = ft.Row(
      spacing=12,
      wrap=True,
    )

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
          fit=ft.BoxFit.FILL,
          border_radius=8
        )
        if self.pack.get("cover")
        else ft.Icon(ft.Icons.ACCOUNT_BOX_ROUNDED, size=96)
      )
    )

    def _on_cover_picked(path: str):
      self._pending_cover = path
      cover_holder.content = ft.Image(
        src=path,
        width=96,
        height=96,
        fit=ft.BoxFit.COVER,
        border_radius=8
      )
      if cover_holder.page:
        cover_holder.update()
    self.app.pick_image(_on_cover_picked)

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
      floating_action_button=ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        foreground_color=wac.TEA_GREEN,
        bgcolor=wac.WA_LIGHT_GREEN,
        content=ft.Text("Add Sticker"),
        on_click=self.create_sticker
      ),
      controls=[
        ft.SafeArea(
          ft.Column(
            [
              # pack cover
              ft.Row(
                [cover_holder],
                alignment=ft.MainAxisAlignment.CENTER
              ),

              # name and author textfield
              ft.Row([
                ft.Column([
                  name,
                  author
                ]),
              ], alignment=ft.MainAxisAlignment.CENTER),

              #TODO: fix the damn centering
              #NOTE: adding wrap to Row breaks the fucking thing
              ft.Container(height=10),
              self.stickers,

              # delete pack button
              ft.Container(height=24),
              ft.Row([
                ft.TextButton(
                  "Delete pack",
                  icon=ft.Icons.DELETE_OUTLINE,
                  style=ft.ButtonStyle(color=ft.Colors.RED_600),
                  on_click=delete
                )
              ], alignment=ft.MainAxisAlignment.END)
            ],
            tight=True,
            spacing=12,
            scroll=ft.ScrollMode.AUTO
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
          ft.Row([
            ft.Column([
              ft.Icon(ft.Icons.ERROR_OUTLINE, size=48),
              ft.Text("Pack not found", size=16),
              ft.Button("Back to home", on_click=lambda _: self.page.navigate("/")),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
          ], alignment=ft.MainAxisAlignment.CENTER),
          expand=True
        )
      ]
    )

  # ---------------------------------------------------- create sticker
  #TODO: fix sticker not filling the container
  async def create_sticker(self, e: ft.Event[ft.Button] | None = None):
    if self.app.total_stickers >= self.app.MAX_STICKERS:
      self.page.show_dialog(ft.SnackBar(ft.Text("You've reached the maximum amount of stickers available.")))
      return

    def add_sticker(image_path: str):
      self.stickers.controls.append(
        ft.Container(
          width=96, height=96,
          blend_mode=ft.BlendMode.CLEAR,
          border=ft.Border.all(1),
          border_radius=6,
          content=ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=[
              ft.Image(
                src=image_path,
                error_content=ft.Icon(ft.Icons.IMAGE),
                fit=ft.BoxFit.FILL
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                  ft.IconButton(
                    ft.Icons.MORE_HORIZ,
                    icon_size=24,
                    bgcolor=wac.TEA_GREEN,
                  )
                ]
              )
            ]
          )
        )
      )

    try:
      image = await ft.FilePicker().pick_files(
        dialog_title="Select an image",
        file_type=ft.FilePickerFileType.IMAGE,
        allow_multiple=False
      )
      if image and image[0].path:
        add_sticker(image[0].path)
      else:
        self.page.show_dialog(ft.SnackBar(ft.Text("Failed to add image as sticker.")))

      if self.pack is None:
        print(f"{ttc.RED}[EditView], self.pack is None")
        return

      #TODO: add proper implementation of ID
      self.pack["ID"] = "YE ID"
    except RuntimeError:
      print(f"{ttc.RED}[EditView] RuntimeError, skipping file picker{ttc.RESET}")
      self.page.show_dialog(ft.SnackBar(ft.Text("Failed to open image picker.")))
