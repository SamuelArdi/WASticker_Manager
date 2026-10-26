import flet as ft

INITIAL_PRODUCTS = [
    {"name": "Desk Lamp", "price": "$24", "on_sale": False},
    {"name": "Wireless Mouse", "price": "$18", "on_sale": True},
    {"name": "Notebook", "price": "$6", "on_sale": False},
]


def format_price(value: float) -> str:
    """Render 24.0 -> '$24', 24.5 -> '$24.50'."""
    if value == int(value):
        return f"${int(value)}"
    return f"${value:,.2f}"


def main(page: ft.Page):
    page.title = "Catalog"
    page.appbar = ft.AppBar(title=ft.Text("Catalog"), center_title=True)

    # Single source of truth for the UI.
    products: list[dict] = [dict(p) for p in INITIAL_PRODUCTS]

    # ---------------------------------------------------------------- cards
    def add_to_cart(product_name: str):
        def handle_click(e: ft.Event[ft.Button]):
            page.show_dialog(ft.SnackBar(ft.Text(f"Added {product_name} to cart")))

        return handle_click

    def product_card(product: dict) -> ft.Control:
        card = ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(product["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(product["price"], color=ft.Colors.OUTLINE),
                        ],
                    ),
                    ft.Button("Buy", on_click=add_to_cart(product["name"])),
                ],
            ),
        )

        if not product["on_sale"]:
            return card

        return ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=[
                card,
                ft.Container(
                    content=ft.Text("SALE", size=10, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED,
                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    border_radius=4,
                    top=-6,
                    right=-6,
                ),
            ],
        )

    product_list = ft.Column(
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    def refresh_list():
        product_list.controls = [product_card(p) for p in products]
        if not products:
            product_list.controls.append(
                ft.Text("No products yet. Tap + to add one.", color=ft.Colors.OUTLINE)
            )
        page.update()

    # ------------------------------------------------------- add-item form
    name_field = ft.TextField(label="Product name", hint_text="e.g. Desk Lamp", autofocus=True)
    price_field = ft.TextField(label="Price", prefix="$", hint_text="0.00")
    sale_switch = ft.Switch(label="On sale", value=False)
    error_text = ft.Text(size=12, color=ft.Colors.ERROR, visible=False)

    def show_error(message: str):
        error_text.value = message
        error_text.visible = True
        page.update()

    def close_dialog(e: ft.Event[ft.Control] | None = None):
        page.pop_dialog()

    def save_product(e: ft.Event[ft.Control] | None = None):
        name = (name_field.value or "").strip()
        raw_price = (price_field.value or "").strip().lstrip("$").strip()

        if not name:
            show_error("Please enter a product name.")
            return
        if any(p["name"].casefold() == name.casefold() for p in products):
            show_error(f"\u201c{name}\u201d is already in the catalog.")
            return
        try:
            price = float(raw_price)
        except ValueError:
            show_error("Please enter a valid price, e.g. 24 or 24.99.")
            return
        if price < 0:
            show_error("Price cannot be negative.")
            return

        products.append(
            {
                "name": name,
                "price": format_price(price),
                "on_sale": bool(sale_switch.value),
            }
        )

        page.pop_dialog()          # close the AlertDialog
        refresh_list()             # rebuild the page from the data
        page.show_dialog(ft.SnackBar(ft.Text(f"Added {name} to the catalog")))

    def open_add_dialog(e: ft.Event[ft.Control] | None = None):
        # reset the form every time the dialog opens
        name_field.value = ""
        price_field.value = ""
        sale_switch.value = False
        error_text.visible = False

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Add product"),
                content=ft.Column(
                    tight=True,
                    spacing=12,
                    width=320,
                    controls=[name_field, price_field, sale_switch, error_text],
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.FilledButton("Add", on_click=save_product),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    # Enter in the price field submits the form.
    price_field.on_submit = save_product

    # ---------------------------------------------------------------- page
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        tooltip="Add product",
        on_click=open_add_dialog,
    )
    page.add(product_list)
    refresh_list()


if __name__ == "__main__":
    ft.run(main)
