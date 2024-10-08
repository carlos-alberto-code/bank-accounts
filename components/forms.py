from time import sleep
import flet as ft
from typing import Optional
from data.accounts_manager import AccountsManager, Customer

accounts = AccountsManager()

class SnackbarMessage(ft.SnackBar):
    def __init__(self, message: str,):
        super().__init__(
            content=ft.Row([ft.Text(message)], alignment=ft.MainAxisAlignment.CENTER),
        )

class FormControlsFactory:

    def create_title_form(self, text: str, icon: Optional[str]):
        return ft.Row(
            [ft.Icon(icon), ft.Text(text)],
            alignment=ft.MainAxisAlignment.START,
        )

    def create_text_field(self, label: str, input_filter: ft.InputFilter, autofocus: bool = False, visible: bool = True, on_change=None) -> ft.TextField:
        return ft.TextField(
            label=label,
            height=40,
            border_radius=10,
            text_size=13,
            prefix_icon=ft.icons.PERSON,
            input_filter=input_filter,
            autofocus=autofocus,
            visible=visible,
            on_change=on_change,
        )

    def create_elevated_button(self, text: str, icon: str, disabled: bool = False, on_click=None) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text, icon=icon,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            disabled=disabled,
            on_click=on_click
        )

class BaseForm(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self._controls_factory = FormControlsFactory()

    @property
    def factory(self):
        return self._controls_factory

class ConfirmationForm(BaseForm):

    def __init__(self, title: str, content: list[ft.Control], on_confirm=None, on_cancel=None, on_dismiss=None):
        super().__init__()
        self._on_confirm = on_confirm
        self._on_cancel = on_cancel
        self.title = self.factory.create_title_form(title, ft.icons.CONFIRMATION_NUM)
        self.content = ft.ResponsiveRow(content)
        self.actions = [
            self.factory.create_elevated_button(
                text='Cancelar', icon=ft.icons.CANCEL,
                on_click=self._on_cancel
            ),
            self.factory.create_elevated_button(
                text='Confirmar', icon=ft.icons.SAVE,
                on_click=self._on_confirm
            ),
        ]
        self.on_dismiss = on_dismiss

    @property
    def on_confirm(self):
        return self._on_confirm

    @on_confirm.setter
    def on_confirm(self, event_function: ft.ControlEvent):
        self._on_confirm = event_function

    @property
    def on_cancel(self):
        return self._on_cancel

    @on_cancel.setter
    def on_cancel(self, event_function: ft.ControlEvent):
        self._on_cancel = event_function

class NewCustomerForm(BaseForm):

    def __init__(self):
        super().__init__()
        self._psurname = self.factory.create_text_field(
            label='Apellido Paterno',
            input_filter=ft.TextOnlyInputFilter(),
            on_change=self._handle_on_change
        )
        self._msurname = self.factory.create_text_field(
            label='Apellido Materno',
            input_filter=ft.TextOnlyInputFilter(),
            on_change=self._handle_on_change
        )
        self._names = self.factory.create_text_field(
            label='Nombre(s)',
            input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]{1,30}$'),
            autofocus=True,
            on_change=self._handle_on_change
        )
        self._account = self.factory.create_text_field(
            label='Número de cuenta',
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self._handle_on_change
        )
        self.title = self.factory.create_title_form('Nuevo cliente', ft.icons.NEW_LABEL)
        self._save_button = self.factory.create_elevated_button(
            text='Guardar', icon=ft.icons.SAVE_ALT,
            disabled=True,
            on_click=self._handle_on_save_click,
        )
        self.content = ft.ResponsiveRow(
            [
                ft.Divider(),
                self._names,
                self._psurname,
                self._msurname,
                self._account
            ],
        )
        self.actions = [
            self.factory.create_elevated_button(
                text='Cancelar', icon=ft.icons.CANCEL,
                on_click=self._handle_on_cancel_click
            ),
            self.factory.create_elevated_button(
                text='Limpiar', icon=ft.icons.CLEAR_ROUNDED,
                on_click=self._handle_on_clean_click
            ),
            self._save_button
        ]

    def reset_values(self):
        self._psurname.value = ''
        self._msurname.value = ''
        self._names.value = ''
        self._account.value = ''

    def _reset_controls(self):
        self._save_button.disabled = True
        self._save_button.update()

    def _handle_on_change(self, event: ft.ControlEvent):
        if self._data_exist:
            self._save_button.disabled = False
            self._save_button.update()
        else:
            self._save_button.disabled = True
            self._save_button.update()

    def _handle_on_cancel_click(self, event: ft.ControlEvent):
        self.reset_values()
        self._reset_controls()
        self.open = False
        event.page.update()

    def _handle_on_clean_click(self, event: ft.ControlEvent):
        self.reset_values()
        self._reset_controls()
        self._names.focus()
        self.update()

    def _handle_on_save_click(self, event: ft.ControlEvent):
        page: ft.Page = event.page
        number = str(self._account.value)
        if self._account_exist(number):
            snackbar = SnackbarMessage('El número de cuenta ya existe!')
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
        else:
            self._open_confirmation_alert(event)

    def _account_exist(self, account: str) -> bool:
        return True if accounts.exists(account) else False

    def _open_confirmation_alert(self, event: ft.ControlEvent):
        page: ft.Page = event.page
        self.customer = Customer(
            apellido_paterno=str(self._psurname.value),
            apellido_materno=str(self._msurname.value),
            nombres=str(self._names.value).strip(),
            numero_de_cuenta=str(self._account.value),
        )
        self.alert_confirmation = ConfirmationForm(
            title='Confirma los datos',
            content=[
                ft.Text(self.customer.full_name),
                ft.Row(
                    [
                        ft.Text('Cuenta:'),
                        ft.Text(self.customer.numero_de_cuenta),
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            on_cancel=self._handle_on_cancel_confirmation_alert,
            on_confirm=self._handle_on_confirm_confirmation_alert
        )
        page.overlay.append(self.alert_confirmation)
        self.alert_confirmation.open = True
        page.update()

    def _handle_on_confirm_confirmation_alert(self, event: ft.ControlEvent):
        accounts.add(self.customer)
        self.alert_confirmation.title = None
        self.alert_confirmation.content = ft.Row(
            [ft.Text('Datos guardados exitosamente!')],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.alert_confirmation.actions.clear()
        self.alert_confirmation.update()

    def _handle_on_cancel_confirmation_alert(self, event: ft.ControlEvent):
        self.open = True
        event.page.update()

    @property
    def _data_exist(self) -> bool:
        return True if self._msurname.value and self._psurname.value and self._names.value and self._account.value else False

class EditCustomerForm(BaseForm):

    def __init__(self):
        super().__init__()
        self._account = self.factory.create_text_field(
            label='Número de cuenta',
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self._handle_on_change
        )
        self.title = self.factory.create_title_form('Editar cliente', ft.icons.EDIT)
        self._search_button = self.factory.create_elevated_button(
            text='Buscar', icon=ft.icons.SAVE_ALT,
            disabled=True,
            on_click=self._handle_on_save_click,
        )
        self.content = ft.ResponsiveRow(
            [
                self._account
            ],
        )
        self.actions = [
            self.factory.create_elevated_button(
                text='Cancelar', icon=ft.icons.CANCEL,
                on_click=self._handle_on_cancel_click
            ),
            self.factory.create_elevated_button(
                text='Limpiar', icon=ft.icons.CLEAR_ROUNDED,
                on_click=self._handle_on_clean_click
            ),
            self._search_button
        ]

    def _exist_data_in_txt_fld(self) -> bool:
        return True if self._account.value else False

    def _handle_on_change(self, event: ft.ControlEvent):
        if self._exist_data_in_txt_fld:
            self._search_button.disabled = False
            self._search_button.update()
        else:
            self._search_button.disabled = True
            self._search_button.update()

    def _handle_on_cancel_click(self, event: ft.ControlEvent):
        self._account.value = ''
        self._search_button.disabled = True
        self._search_button.update()
        self.open = False
        event.page.update()

    def _handle_on_clean_click(self, event: ft.ControlEvent):
        self._account.value = ''
        self._search_button.disabled = True
        self._search_button.update()
        self._account.focus()
        self.update()

    def _account_exist(self, account: str) -> bool:
        return True if accounts.exists(account) else False

    def _handle_on_save_click(self, event: ft.ControlEvent):
        page: ft.Page = event.page
        number = str(self._account.value)
        if self._account_exist(number):
            # Actualizar la tabla para mostrar los datos del cliente con esa cuenta y habilitar los campos de la tabla para editar
            pass
        else:
            self._account.error_text = 'El número de cuenta no existe!'

