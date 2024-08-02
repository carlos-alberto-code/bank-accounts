import flet as ft

from view.account_form      import Form
from view.table_accounts    import TableAccounts
from data.accounts_manager  import AccountsManager
from view.appbar_actions    import add_button, delete_button, edit_button, searcher

class AccountController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.accounts = AccountsManager()
        self.form = Form()
        self.table_accounts = TableAccounts()
    
    def setup_appbar(self):
        self.page.appbar = ft.AppBar(
            title=ft.Column(
                [
                    ft.Row(
                        [
                            add_button,
                            edit_button,
                            delete_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [searcher],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            center_title=True,
            toolbar_height=120
        )

    def setup_components(self):
        add_button.on_click     = self.handle_on_add_button_click
        edit_button.on_click    = self.handle_on_edit_button_click
        delete_button.on_click  = self.handle_on_delete_button_click
        searcher.on_change      = self.handle_on_searcher_change
        self.setup_appbar()
        self.page.overlay.append(self.form)
        self.page.add(self.table_accounts)

    def handle_on_add_button_click(self, event: ft.ControlEvent):
        self.form.reset()
        self.form.open = True
        self.page.update()
    
    def handle_on_edit_button_click(self, event: ft.ControlEvent):
        print('edit')

    def handle_on_delete_button_click(self, event: ft.ControlEvent):
        print('delete')
    
    def handle_on_searcher_change(self, event: ft.ControlEvent):
        print('\n\n')
        txt_field: ft.TextField = event.control
        search_term = str(txt_field.value).strip()
        results = self.accounts.search_customers(search_term)
        print(results)
