import flet as ft
from view.table_accounts import TableAccounts
from view.appbar_actions import add_button, edit_button, delete_button, searcher

def main(page: ft.Page):

    page.theme_mode           = ft.ThemeMode.LIGHT
    page.vertical_alignment   = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme                = ft.Theme(color_scheme_seed='green')

    page.appbar = ft.AppBar(
        title=searcher,
        center_title=True,
        actions=[
            add_button, edit_button, delete_button, ft.Container(width=10)
        ],
        elevation=50,
        toolbar_height=50,
    )

    table_accounts = TableAccounts()
    total_accounts = ft.Text(f'Existen {table_accounts.total_accounts} cuentas en total'.capitalize())
    page.add(
        ft.Row(
            [total_accounts],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        table_accounts
    )

ft.app(target=main)