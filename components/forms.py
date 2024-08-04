import flet as ft
from typing import Optional
from data.accounts_manager import AccountsManager, Customer

accounts = AccountsManager()

class FormControlsFactory:

    def create_title_form(self, text: str, icon: Optional[str]):
        return ft.Row(
            [ft.Icon(icon), ft.Text(text)]
        )
    
    def create_text_field(self, label: str, input_filter: ft.InputFilter, autofocus: bool = False, visible: bool = True) -> ft.TextField:
        return ft.TextField(
            label=label,
            height=40,
            border_radius=10,
            text_size=13,
            prefix_icon=ft.icons.PERSON,
            input_filter=input_filter,
            autofocus=autofocus,
            visible=visible
        )

    def create_elevated_button(self, text: str, icon: str, on_click=None) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text, icon=icon,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=on_click
        )

class BaseForm(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self._controls_factory = FormControlsFactory()
    
    @property
    def factory(self):
        return self._controls_factory
    
    def open_form(self):
        self.open = True
        self.update()
    
    def close_form(self):
        self.open = False
        self.update()
    

class ConfirmationForm(ft.AlertDialog):

    def __init__(self, customer: Customer, on_confirm=None, on_cancel=None):
        super().__init__()
        self._factory = FormControlsFactory()
        self._on_confirm = on_confirm
        self.title = self._factory.create_title_form('Confirmación', ft.icons.CONFIRMATION_NUM)
        self.content = ft.ResponsiveRow(
            [
                ft.Text('Asegurate de que los datos sean correctos!'),
                ft.Text(f'Persona: {customer.nombres.capitalize()} {customer.apellido_paterno.capitalize()} {customer.apellido_materno.capitalize()}'),
                ft.Text(f'Cuenta: {customer.numero_de_cuenta}')
            ]
        )
        self.actions = [
            self._factory.create_elevated_button(
                text='Cancelar', icon=ft.icons.CANCEL,
                on_click=on_cancel
            ),
            self._factory.create_elevated_button(
                text='Confirmar', icon=ft.icons.SAVE,
                on_click=self.on_confirm
            )
        ]

    @property
    def on_confirm(self):
        return self._on_confirm
    
    @on_confirm.setter
    def on_confirm(self, event_function: ft.ControlEvent):
        self._on_confirm = event_function
    
    def open_form(self):
        self.open = True
        self.update()
    
    def close_form(self):
        self.open = False
        self.update()
    
class NewCustomerForm(BaseForm):

    def __init__(self):
        super().__init__()
        self._psurname = self.factory.create_text_field(
            label='Apellido Paterno',
            input_filter=ft.TextOnlyInputFilter(),
            autofocus=True
        )
        self._msurname = self.factory.create_text_field(
            label='Apellido Materno',
            input_filter=ft.TextOnlyInputFilter()
        )
        self._names = self.factory.create_text_field(
            label='Nombres',
            input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]+$')
        )
        self._account = self.factory.create_text_field(
            label='Número de cuenta',
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.title = self.factory.create_title_form('Nuevo cliente', ft.icons.NEW_LABEL)
        self.content = ft.ResponsiveRow(
            [
                ft.Divider(),
                self._psurname,
                self._msurname,
                self._names,
                self._account
            ],
        )
        self.actions = [
            self.factory.create_elevated_button('Cancelar', ft.icons.CANCEL, self._handle_on_cancel_click),
            self.factory.create_elevated_button('Limpiar', ft.icons.CLEAR_ALL_ROUNDED, self._handle_on_clean_click),
            self.factory.create_elevated_button('Guardar', ft.icons.SAVE_ALT, self._handle_on_save_click)
        ]
    
    def reset(self):
        self._psurname.value = ''
        self._msurname.value = ''
        self._names.value = ''
        self._account.value = ''
    
    def _handle_on_cancel_click(self, event: ft.ControlEvent):
        self.reset()
        self.open = False
        self.update()
    
    def _handle_on_clean_click(self, event: ft.ControlEvent):
        self.reset()
        self._psurname.focus()
        self.update()
    
    def _handle_on_save_click(self, event: ft.ControlEvent):
        if not self._data_exist:
            print('Los datos no existen: marcar los controles que no tengan datos en rojo')
        if self._data_exist:
            customer = Customer(
                apellido_paterno=str(self._psurname.value),
                apellido_materno=str(self._msurname.value),
                nombres=str(self._names.value),
                numero_de_cuenta=str(self._account.value)
            )
            self.alert_confirmation = ConfirmationForm(customer, self._handle_on_confirm_clik, on_cancel=self._handle_on_cancel_click_in_alert)
            page: ft.Page = event.page
            page.overlay.append(self.alert_confirmation)
            event.page.update()
            self.alert_confirmation.open_form()
    
    def _handle_on_confirm_clik(self, event: ft.ControlEvent):
        print('Datos confirmados!')
        self.alert_confirmation.close_form()

    def _handle_on_cancel_click_in_alert(self, event: ft.ControlEvent):
        # self.alert_confirmation.close_form()
        self.open_form()
        event.page.update()

    @property
    def _data_exist(self) -> bool:
        return True if self._msurname.value and self._psurname.value and self._names.value and self._account.value else False
    