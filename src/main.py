from backend import lib
import flet as ft

def main(page: ft.Page):
  page.title = "Flet + C++ (nanobind)"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER

  page.add(
    ft.Column(
      [
        
      ],
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
  )

if __name__ == "__main__":
  ft.run(main)
