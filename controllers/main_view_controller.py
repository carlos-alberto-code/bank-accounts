import flet as ft

from components.accounts_table    import AccountsTable
from components.forms             import NewCustomerForm
from data.accounts_manager        import AccountsManager
from components.appbar_actions    import add_button, delete_button, searcher, restart_button

class AccountsViewController:

    def __init__(self, page: ft.Page):
        self.page = page
        self.accounts = AccountsManager()
        self.new_customer_form = NewCustomerForm()
        self.table_accounts = AccountsTable(
            column_names=self.accounts.columns,
            customers=self.accounts.get_all()
        )

    def _setup_appbar(self):
        self.page.appbar = ft.AppBar(
            title=ft.Column(
                [
                    ft.Row(
                        [
                            add_button,
                            delete_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [searcher, restart_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            center_title=True,
            toolbar_height=120
        )

    def setup_components(self):
        searcher.on_change          = self._handle_on_searcher_change
        add_button.on_click         = self._handle_on_add_button_click
        delete_button.on_click      = self._handle_on_delete_button_click
        restart_button.on_click     = self.handle_on_click_refresh_button
        self._setup_appbar()
        self.page.overlay.append(self.new_customer_form)
        self.page.add(self.table_accounts)

    def handle_on_click_refresh_button(self, event: ft.ControlEvent):
        self.table_accounts.customers = self.accounts.get_all()
        self.table_accounts.update()
        searcher.value = ''
        self.page.update()

    def _handle_on_add_button_click(self, event: ft.ControlEvent):
        self.new_customer_form.reset_values()
        self.new_customer_form.open = True
        self.page.update()

    def _handle_on_delete_button_click(self, event: ft.ControlEvent):
        self.table_accounts.active_deleting()
        self.page.update()

    def _handle_on_searcher_change(self, event: ft.ControlEvent):
        text = str(searcher.value)
        results = self.accounts.search(text)
        self.table_accounts.customers = results
        self.table_accounts.update()
