import flet as ft

from components.accounts_table    import AccountsTable
from components.forms             import NewCustomerForm
from data.accounts_manager        import AccountsManager
from components.appbar_actions    import add_button, delete_button, searcher, import_data_button

class AccountsViewController:

    def __init__(self, page: ft.Page):
        self.page = page
        self.accounts = AccountsManager()
        self.new_customer_form = NewCustomerForm()
        self.table_accounts = AccountsTable(
            column_names=self.accounts.columns,
            customers=self.accounts.get_all()
        )
        self.import_button = ft.PopupMenuButton()
        if self.accounts.exists_file:
            import_data_button.on_click = self.handle_on_import_data_button_click
            self.import_button.icon = ft.icons.MORE_VERT
            self.import_button.tooltip = 'Opciones'
            self.import_button.items = [import_data_button]
        # if self.accounts.exists_file:
        #     self.import_button.visible = False

    def _setup_appbar(self):
        self.page.appbar = ft.AppBar(
            title=ft.Column(
                [
                    ft.Row(
                        [
                            add_button,
                            delete_button,
                            self.import_button
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
        searcher.on_change          = self._handle_on_searcher_change
        add_button.on_click         = self._handle_on_add_button_click
        delete_button.on_click      = self._handle_on_delete_button_click
        self._setup_appbar()
        self.page.overlay.append(self.new_customer_form)
        self.page.add(self.table_accounts)

    def handle_on_import_data_button_click(self, event: ft.ControlEvent):
        print('Importar datos')

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
