import flet as ft
from data.accounts_manager import Customer
from components.forms import ConfirmationForm

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
    
    def active_editing(self) -> None:
        if self.rows:
            for row in self.rows:
                for cell in row.cells[:-1]:
                    cell.show_edit_icon = True
                    cell.on_tap = self.handle_on_edit_tap
            self.update()
    
    def disable_editing(self) -> None:
        if self.rows:
            for row in self.rows:
                for cell in row.cells[:-1]:
                    cell.show_edit_icon = False
                    cell.on_tap = None
            self.update()
    
    def _create_columns(self) -> list[ft.DataColumn]:
        return [
            ft.DataColumn(
                label=ft.Text(column_name),
                tooltip=f'Ordenar por {column_name.lower()}',
                on_sort=self.handle_on_sort
            )
            for column_name in self._column_names
        ]

    def _create_rows(self) -> list[ft.DataRow]:
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(customer.apellido_paterno, size=13), data={'column': 'apellido paterno', 'value': customer.apellido_paterno, 'row': customer}),
                    ft.DataCell(ft.Text(customer.apellido_materno, size=13), data={'column': 'apellido materno', 'value': customer.apellido_materno, 'row': customer}),
                    ft.DataCell(ft.Text(customer.nombres, size=13), data={'column': 'nombres', 'value': customer.nombres, 'row': customer}),
                    ft.DataCell(
                        ft.Row(
                            [ft.Text(customer.numero_de_cuenta, size=13), ft.Icon(ft.icons.COPY, size=13)],
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
    
    def _create_text_field(self, value: str, on_submit=None) -> ft.TextField:
        return ft.TextField(
            value=value,
            text_style=ft.TextStyle(size=13),
            color='green',
            border_radius=5,
            border=ft.InputBorder.NONE,
            text_align=ft.TextAlign.CENTER,
            on_submit=on_submit,
            autofocus=True,
        )
    
    def _show_alert_message(self, event: ft.ControlEvent) -> None:
        page: ft.Page = event.page
        confirmation = ConfirmationForm(
            title='Confirmación',
            content=[ft.Text('¿Estás seguro de que deseas guardar los cambios?')],
            on_confirm=lambda event: print('Confirmado'),
            on_cancel=lambda event: print('Cancelado'),
        )
        page.overlay.append(confirmation)
        confirmation.open = True
        page.update()

    def _handle_on_submit(self, event: ft.ControlEvent) -> None:
        # txt_field: ft.TextField = event.control
        # new_text_value: str = str(txt_field.value)
        # txt_field.read_only = True
        # txt_field.text_align = ft.TextAlign.START
        # txt_field.color = 'black'
        # txt_field.update()
        self._show_alert_message(event)
        
    
    def handle_on_edit_tap(self, event: ft.ControlEvent) -> None:
        cell: ft.DataCell = event.control
        current_text_value: str = cell.content.value # type: ignore
        cell.content = self._create_text_field(current_text_value, on_submit=self._handle_on_submit)
        self.disable_editing()
        cell.update()
    