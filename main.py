import flet as ft
from controllers.account_controller import AccountController

def main(page: ft.Page):
    account_controller = AccountController(page)
    account_controller.setup()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed='green')
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

ft.app(target=main)