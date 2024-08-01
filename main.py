import flet as ft
from view.account_form   import Form
from view.table_accounts import TableAccounts
from view.appbar_actions import add_button, edit_button, delete_button, searcher

def main(page: ft.Page):

    def handle_on_save_form(event: ft.ControlEvent):
        pass

    def handle_on_add_button_click(event: ft.ControlEvent):
        form.restet()
        form.open = True
        page.overlay.append(form)
        page.update()

    def handle_on_edit_button_click(event: ft.ControlEvent):
        print('edit')

    def handle_on_delete_button_click(event: ft.ControlEvent):
        print('delete')

    page.theme_mode           = ft.ThemeMode.LIGHT
    page.vertical_alignment   = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme                = ft.Theme(color_scheme_seed='green')

    add_button.on_click       = handle_on_add_button_click
    edit_button.on_click      = handle_on_edit_button_click
    delete_button.on_click    = handle_on_delete_button_click

    form = Form(on_save=handle_on_save_form)

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