import flet as ft
from data.accounts_manager import AccountsManager, Customer

accounts = AccountsManager()

class AlertForm(ft.AlertDialog):
    def __init__(self):
        super().__init__()
    
    def open_form(self):
        self.open = True
        self.update()
    
    def close_form(self):
        self.open = False
        self.update()
    
    def create_elevated_button(self, text: str, icon: str, on_click=None) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text, icon=icon,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=on_click
        )

class FormConfirmation(AlertForm):
    def __init__(self, title: str, content: ft.Control, actions: list[ft.Control]):
        super().__init__()
        self.title = ft.Row(
            [ft.Icon(ft.icons.CONFIRMATION_NUM), ft.Text(f'{title}')],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.content = content
        self.actions = actions

class Form(AlertForm):
    def __init__(self):
        super().__init__()
    
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

class NewCustomerForm(Form):

    def __init__(self):
        super().__init__()
        self._paternal_surname = self.create_text_field(
            label='Apellido Paterno',
            input_filter=ft.TextOnlyInputFilter(),
            autofocus=True
        )
        self._maternal_surname = self.create_text_field(
            label='Apellido Materno',
            input_filter=ft.TextOnlyInputFilter()
        )
        self._customer_names = self.create_text_field(
            label='Nombres',
            input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]+$')
        )
        self._account_number = self.create_text_field(
            label='Número de cuenta',
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.title = ft.Row(
            [
                ft.Icon(ft.icons.PERSON_ADD),
                ft.Text('Nuevo cliente', style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD))
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.content = ft.ResponsiveRow(
            [
                ft.Divider(),
                self._paternal_surname,
                self._maternal_surname,
                self._customer_names,
                self._account_number
            ],
        )
        self.actions = [
            self.create_elevated_button('Cancelar', ft.icons.CANCEL, self._handle_on_cancel_click),
            self.create_elevated_button('Limpiar', ft.icons.CLEAR_ALL_ROUNDED, self._handle_on_clean_click),
            self.create_elevated_button('Guardar', ft.icons.SAVE_ALT, self._handle_on_save_click)
        ]
    
    def reset(self):
        self._paternal_surname.value = ''
        self._maternal_surname.value = ''
        self._customer_names.value = ''
        self._account_number.value = ''
    
    def _handle_on_cancel_click(self, event: ft.ControlEvent):
        self.reset()
        self.open = False
        self.update()
    
    def _handle_on_clean_click(self, event: ft.ControlEvent):
        self.reset()
        self._paternal_surname.focus()
        self.update()
    
    def _handle_on_save_click(self, event: ft.ControlEvent):
        customer = Customer(
            apellido_paterno=str(self._paternal_surname.value),
            apellido_materno=str(self._maternal_surname.value),
            nombres=str(self._customer_names.value),
            numero_de_cuenta=str(self._account_number.value)
        )
        if self._data_exist:
            self.alert_confirmation = FormConfirmation(
                title='Confirmación',
                actions=[
                    self.create_elevated_button('Cancelar', ft.icons.CANCEL, self._handle_on_cancel_click_in_alert),
                    self.create_elevated_button('Confirmar', ft.icons.SAVE),
                ],
                content=ft.Text(f'Asegurate de que los datos sean correctos:\nNombre completo: {customer.apellido_paterno.capitalize()} {customer.apellido_materno.capitalize()} {customer.nombres.capitalize()}\nNúmero de cuenta: {customer.numero_de_cuenta}')
            )
            page: ft.Page = event.page
            self.alert_confirmation.open = True
            page.overlay.append(self.alert_confirmation)
            page.update()

    @property
    def _data_exist(self) -> bool:
        return True if self._maternal_surname.value and self._paternal_surname.value and self._customer_names.value and self._account_number.value else False
    
    def _handle_on_cancel_click_in_alert(self, event: ft.ControlEvent):
        self.alert_confirmation.open = False
        self.open_form()