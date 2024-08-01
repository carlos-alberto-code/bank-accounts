import flet as ft
from data.accounts import Accounts

def _create_data_column(label: str, on_sort=None) -> ft.DataColumn:
    return ft.DataColumn(
        label=ft.Row([ft.Text(label, text_align=ft.TextAlign.CENTER)], alignment=ft.MainAxisAlignment.CENTER),
        tooltip=f'Ordenar por {label.lower()}',
        on_sort=on_sort
    )

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


class TableAccounts(ft.DataTable):

    def __init__(self):
        self._accounts = Accounts()
        super().__init__(
            data_text_style=ft.TextStyle(size=14),
            border_radius=10,
            border=ft.border.all(width=1),
            horizontal_lines=ft.BorderSide(width=1),
            vertical_lines=ft.BorderSide(width=1),
            columns=[
                _create_data_column(
                    label=column,
                    on_sort=lambda e: print('Ordenado')
                ) for column in self._accounts.column_names
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['Apellido Paterno'])),
                        ft.DataCell(ft.Text(row['Apellido Materno'])),
                        ft.DataCell(ft.Text(row['Nombres'])),
                        ft.DataCell(
                            ft.Row(
                                [ft.Text(row['Numero de Cuenta']), ft.Icon(ft.icons.COPY)],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            on_tap=_handle_on_click_cell
                        )
                    ]
                ) for index, row in self._accounts.rows
            ]
        )
    
    def add_account(
            self,
            apellido_paterno: str,
            apellido_materno: str,
            nombres: str,
            numero_de_cuenta: str,
    ) -> None:
        self._accounts.add_account(
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            nombres=nombres,
            numero_de_cuenta=numero_de_cuenta
        )
    
    def delete_account(self, account_numer: str):
        self._accounts.remove_account(account_number=account_numer)
