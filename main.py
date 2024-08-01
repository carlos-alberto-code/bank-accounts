import flet as ft
from view.table_accounts import TableAccounts
from view.options import add_button, edit_button, delete_button, searcher

def main(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode =  ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed='green')

    page.appbar = ft.AppBar(
        title=searcher,
        center_title=True,
        actions=[
            add_button, edit_button, delete_button, ft.Container(width=10)
        ],
        elevation=50,
        toolbar_height=50,
    )

    page.add(
        TableAccounts()
    )

ft.app(target=main)