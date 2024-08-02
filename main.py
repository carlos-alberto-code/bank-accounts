import flet as ft
from data.accounts_manager import AccountsManager, Customer
from controllers.accounts_view_controller import AccountsViewController

def main(page: ft.Page):
    account_controller = AccountsViewController(page)
    account_controller.setup_components()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed='green')
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.update()

ft.app(target=main)