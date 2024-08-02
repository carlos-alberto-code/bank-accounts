import flet as ft
from data.accounts_manager import Customer

def _create_snackbar(message: str) -> ft.SnackBar:
    return ft.SnackBar(
        content=ft.Row([ft.Text(message)], alignment=ft.MainAxisAlignment.CENTER),
    )

def _show_message(event: ft.ControlEvent) -> None:
    snackbar = _create_snackbar(f'Número de cuenta copiado!')
    snackbar.open = True
    page: ft.Page = event.page
    page.overlay.append(snackbar)
    page.update()

def _handle_on_click_cell(event: ft.ControlEvent) -> None:
    page: ft.Page = event.page
    page.set_clipboard(str(event.control.content.controls[0].value))
    _show_message(event)


class AccountsTable(ft.DataTable):

    def __init__(self, column_names: list[str], customers: list[Customer]) -> None:
        self._customers: list[Customer] = customers
        self._column_names: list[str] = column_names
        self._sort_columns_states: dict[str, bool] = {column_name.lower(): False for column_name in self._column_names}
        super().__init__(
            data_text_style=ft.TextStyle(size=14),
            border_radius=10,
            border=ft.border.all(width=1),
            horizontal_lines=ft.BorderSide(width=1),
            vertical_lines=ft.BorderSide(width=1),
            columns=self._create_columns(),
            rows=self._create_rows(),
        )
    
    @property
    def customers(self) -> list[Customer]:
        return self._customers
    
    @customers.setter
    def customers(self, customers: list[Customer]) -> None:
        self._customers = customers
        self.rows = self._create_rows()
    
    def _create_columns(self) -> list[ft.DataColumn]:
        return [
            ft.DataColumn(
                label=ft.Text(column_name, weight=ft.FontWeight.BOLD),
                tooltip=f'Ordenar por {column_name.lower()}',
                on_sort=self.handle_on_sort
            )
            for column_name in self._column_names
        ]

    def _create_rows(self) -> list[ft.DataRow]:
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(customer.apellido_paterno)),
                    ft.DataCell(ft.Text(customer.apellido_materno)),
                    ft.DataCell(ft.Text(customer.nombres)),
                    ft.DataCell(
                        ft.Row(
                            [ft.Text(customer.numero_de_cuenta), ft.Icon(ft.icons.COPY)],
                        ),
                        on_tap=_handle_on_click_cell,
                    ),
                ]
            ) for customer in self.customers
        ]
    
    def handle_on_sort(self, event: ft.ControlEvent) -> None:
        sorts = {
            'apellido paterno': lambda customer: customer.apellido_paterno,
            'apellido materno': lambda customer: customer.apellido_materno,
            'nombres': lambda customer: customer.nombres,
            'numero de cuenta': lambda customer: customer.numero_de_cuenta,
        }
        col_name: str = event.control.label.value.lower()
        if col_name.lower() in sorts:
            sort = sorts[col_name]
            self._sort_columns_states[col_name] = not self._sort_columns_states[col_name]
            self._customers.sort(key=sort, reverse=self._sort_columns_states[col_name])
            self.rows = self._create_rows()
            self.update()
    