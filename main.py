import flet as ft
from view.view import shape_content

def main(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode =  ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed='green')

    page.appbar = ft.AppBar(
        title=ft.Text('Cuentas'),
        center_title=True,
    )

    page.add(
        ft.Divider(),
        shape_content
    )

ft.app(target=main)