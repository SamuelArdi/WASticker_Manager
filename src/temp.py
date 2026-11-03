
class AppMain():
  def __init__(self, page: ft.Page):
    self.page = page

    # add file picker service into the app
    self.file_picker = ft.FilePicker()
    self.page.services.append(self.file_picker)

    self.pack_column = ft.Column(
      spacing=12,
      horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
      scroll=ft.ScrollMode.AUTO,
      expand=True
    )

    self.page.on_route_change = self.route_change 
    self.page.on_view_pop = self.view_pop

    self.route_change()

  # ---------------------------------------------------- page

  def _build_appbar(self) -> ft.AppBar:
    return ft.AppBar(
      title=ft.Text("Sticker Packs", color=wac.TEA_GREEN),
      leading=ft.IconButton(ft.Icons.MENU, icon_color=wac.TEA_GREEN),
      bgcolor=wac.WA_LIGHT_GREEN,
      adaptive=True,
      actions=[
        ft.IconButton(ft.Icons.SEARCH, icon_color=wac.TEA_GREEN),
        ft.IconButton(ft.Icons.SETTINGS, icon_color=wac.TEA_GREEN, on_click=lambda _: self.page.navigate("/settings"))
      ]
    )

  def _build_fab(self) -> ft.FloatingActionButton:
    return ft.FloatingActionButton(
      icon=ft.Icon(ft.Icons.ADD),
      foreground_color=wac.TEA_GREEN,
      bgcolor=wac.WA_LIGHT_GREEN,
      content=ft.Text("Create Pack"),
      on_click=self.create_pack
    )

  # ---------------------------------------------------- function
  def create_pack(self, e: ft.Event[ft.Button] | None = None):
    #TODO: improve the layout of the dialog

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

      packs.append({
        "cover": cover[0] if cover else None,
        "name": name.value.strip(),
        "author": author.value.strip() or "Unknown",
        "date": datetime.today()
      })
      self.page.pop_dialog()
      self._rebuild()
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

  # ---------------------------------------------------- route changes
  #TODO: add route change for navigation
  #NOTE: add SafeArea
  # self.page.add(self.pack_column)
  def route_change(self, e: ft.RouteChangeEvent | None = None):
    self.page.views.clear()
    self.page.views.append(
      ft.View(
        route="/",
        controls=[
          ft.SafeArea(self.pack_column, expand=True)
        ],
        floating_action_button=self._build_fab(),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
        appbar=self._build_appbar()
      )
    )
    self._rebuild()
    self.page.update()

  async def view_pop(self, e: ft.ViewPopEvent):
    if e.view is not None and e.view in self.page.views:
      self.page.views.remove(e.view)
    if self.page.views:
      await self.page.push_route(self.page.views[-1].route)
    
  def edit_pack(self, pack):
    return
