import flet as ft
from view.table_accounts import table

def main(page: ft.Page):
    page.theme_mode =  ft.ThemeMode.LIGHT
    page.add(table)

ft.app(target=main)