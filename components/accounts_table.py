from typing import Optional
import flet as ft
from data.accounts_manager import Customer
from data.accounts_manager import AccountsManager
from components.forms import ConfirmationForm

def _create_snackbar(message: str) -> ft.SnackBar:
    return ft.SnackBar(
        content=ft.Row([ft.Text(message)], alignment=ft.MainAxisAlignment.CENTER),
    )

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
        self._customer_selected: Optional[Customer] = None
        self._column_selected: Optional[str] = None

    @property
    def customers(self) -> list[Customer]:
        return self._customers

    @customers.setter
    def customers(self, customers: list[Customer]) -> None:
        self._customers = customers
        self.rows = self._create_rows()
    
    def active_editing(self) -> None:
        self._set_editing(True)
    
    def disable_editing(self) -> None:
        self._set_editing(False)

    def _set_editing(self, enable: bool) -> None:
        if self.rows:
            for row in self.rows:
                for cell in row.cells[:-1]:
                    cell.show_edit_icon = enable
                    cell.on_tap = self._handle_on_cell_click if enable else None
            self.update()
    
    def active_deleting(self) -> None:
        self._set_deleting(True)
    
    def disable_deleting(self) -> None:
        self._set_deleting(False)
    
    def _set_deleting(self, enable: bool) -> None:
        if self.rows and enable:
            for row in self.rows:
                cell = row.cells[-1]
                cell.content.controls[1].name = 'delete'
                cell.content.controls[1].size = 18
                cell.on_tap = self._handle_deleting if enable else None
            self.update()
    
    def _create_columns(self) -> list[ft.DataColumn]:
        return [
            ft.DataColumn(
                label=ft.Text(column_name),
                tooltip=f'Ordenar por {column_name.lower()}',
                on_sort=self._handle_on_sort
            )
            for column_name in self._column_names
        ]

    def _create_rows(self) -> list[ft.DataRow]:
        return [
            ft.DataRow(
                cells=[
                    self._create_data_cell(customer.apellido_paterno, 'apellido paterno', customer),
                    self._create_data_cell(customer.apellido_materno, 'apellido materno', customer),
                    self._create_data_cell(customer.nombres, 'nombres', customer),
                    self._create_copy_cell(customer.numero_de_cuenta, {'column': 'numero de cuenta', 'value': customer.numero_de_cuenta, 'row': customer}),
                ]
            ) for customer in self.customers
        ]
    
    def _create_data_cell(self, value: str, column_name: str, customer: Customer) -> ft.DataCell:
        return ft.DataCell(
            ft.Text(value, size=13),
            data={'column': column_name, 'value': value, 'row': customer}
        )

    def _create_copy_cell(self, value: str, data: dict) -> ft.DataCell:
        return ft.DataCell(
            ft.Row(
                [ft.Text(value, size=13), ft.Icon(ft.icons.COPY, size=13)],
            ),
            on_tap=self._handle_on_copy,
            data=data
        )
    
    def _handle_on_sort(self, event: ft.ControlEvent) -> None:
        sorts = {
            'apellido paterno': lambda customer: customer.apellido_paterno,
            'apellido materno': lambda customer: customer.apellido_materno,
            'nombres': lambda customer: customer.nombres,
            'numero de cuenta': lambda customer: customer.numero_de_cuenta,
        }
        col_name: str = event.control.label.value.lower()
        if col_name in sorts:
            sort = sorts[col_name]
            self._sort_columns_states[col_name] = not self._sort_columns_states[col_name]
            self._customers.sort(key=sort, reverse=self._sort_columns_states[col_name])
            self.rows = self._create_rows()
            self.update()
    
    def _create_text_field(self, value: str, on_submit=None, on_blur=None) -> ft.TextField:
        return ft.TextField(
            value=value,
            text_style=ft.TextStyle(size=13),
            color='blue',
            border_radius=5,
            border=ft.InputBorder.NONE,
            text_align=ft.TextAlign.CENTER,
            on_submit=on_submit,
            autofocus=True,
            on_blur=on_blur,
        )
    
    def _handle_on_cancel_alert(self, event: ft.ControlEvent) -> None:
        self.disable_editing()

    def _handle_on_confirm_alert(self, event: ft.ControlEvent):
        pass
    
    def _show_alert_message(self, event: ft.ControlEvent) -> None:
        page: ft.Page = event.page
        confirmation = ConfirmationForm(
            title='Confirmación',
            content=[ft.Text('¿Estás seguro de que deseas guardar los cambios?')],
            on_confirm=self._handle_on_confirm_alert,
            on_cancel=self._handle_on_cancel_alert,
        )
        self._change_alert_color(confirmation, 'blue')
        page.overlay.append(confirmation)
        confirmation.open = True
        page.update()

    def _handle_on_submit(self, event: ft.ControlEvent) -> None:
        self._show_alert_message(event)
        
    def _handle_on_cell_click(self, event: ft.ControlEvent) -> None:
        self._current_cell: ft.DataCell = event.control
        current_text_value: str = event.control.content.value
        self._current_cell.content = self._create_text_field(current_text_value, on_submit=self._handle_on_submit, on_blur=self._handle_on_submit)
        self.disable_editing()
        self._current_cell.update()

    def _handle_on_copy(self, event: ft.ControlEvent) -> None:
        page: ft.Page = event.page
        page.set_clipboard(str(event.control.content.controls[0].value))
        self._show_message(event)
    
    def _show_message(self, event: ft.ControlEvent) -> None:
        snackbar = _create_snackbar('Número de cuenta copiado!')
        snackbar.open = True
        page: ft.Page = event.page
        page.overlay.append(snackbar)
        page.update()

    # Manejo del evento de eliminación

    def _handle_deleting(self, event: ft.ControlEvent):
        cell: ft.DataCell = event.control
        self._show_delete_alert(event)
    
    def _show_delete_alert(self, event: ft.ControlEvent):
        page: ft.Page = event.page
        cell: ft.DataCell = event.control
        if cell.data:
            self._customer_to_deleting: Customer = cell.data['row']
        self._delete_alert = ConfirmationForm(
            title='Elminar cuenta',
            content=[
                ft.Text('Confirma la eliminación del usuario:'),
                ft.Text(f'- {self._customer_to_deleting.full_name}'),
                ft.Text(f'- Número de cuenta: {self._customer_to_deleting.numero_de_cuenta}'),
            ],
            on_cancel=self._handel_on_delete_cancel,
            on_confirm=self._handel_on_delete_confirm,
        )
        self._change_alert_color(self._delete_alert, 'red')
        page.overlay.append(self._delete_alert)
        self._delete_alert.open = True
        page.update()
    
    def _change_alert_color(self, alert: ConfirmationForm, color: str) -> None:
        alert.shadow_color = color
        alert.surface_tint_color = color
        
    def _handel_on_delete_cancel(self, event: ft.ControlEvent) -> None:
        self._delete_alert.open = False
        event.page.update()
    
    def _handel_on_delete_confirm(self, event: ft.ControlEvent) -> None:
        # self._delete_alert.open = False
        accounts = AccountsManager()
        accounts.remove(str(self._customer_to_deleting.numero_de_cuenta))
        self._delete_alert.title = None
        self._delete_alert.content = ft.Text('Usuario eliminado correctamente')
        self._delete_alert.actions = [ft.ElevatedButton('Ok', on_click=self._handel_on_delete_cancel)]
        self._delete_alert.update()
        self.customers = accounts.get_all()
        self.update()