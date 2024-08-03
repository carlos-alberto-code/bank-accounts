import flet as ft
from data.accounts_manager import AccountsManager, Customer

accounts = AccountsManager()

class Form(ft.AlertDialog):
    def __init__(self):
        super().__init__()
    
    def open_form(self) -> None:
        self.open = True
        self.update()
    
    def close_form(self) -> None:
        self.open = False
        self.update()
    
    def _create_elevated_button(self, text: str, icon: str, on_click=None) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text, icon=icon,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=on_click
        )
    
    def _create_text_field(self, label: str, input_filter: ft.InputFilter, autofocus: bool = False, visible: bool = True) -> ft.TextField:
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
        self._paternal_surname = self._create_text_field(
            label='Apellido Paterno',
            input_filter=ft.TextOnlyInputFilter(),
            autofocus=True
        )
        self._maternal_surname = self._create_text_field(
            label='Apellido Materno',
            input_filter=ft.TextOnlyInputFilter()
        )
        self._customer_names = self._create_text_field(
            label='Nombres',
            input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]+$')
        )
        self._account_number = self._create_text_field(
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
            self._create_elevated_button('Cancelar', ft.icons.CANCEL, self._handle_on_cancel),
            self._create_elevated_button('Limpiar', ft.icons.CLEAR_ALL_ROUNDED, self._handle_on_clean),
            self._create_elevated_button('Guardar', ft.icons.SAVE_ALT, self._handle_on_save)
        ]
    
    def reset(self):
        self._paternal_surname.value = ''
        self._maternal_surname.value = ''
        self._customer_names.value = ''
        self._account_number.value = ''
    
    def _handle_on_cancel(self, event: ft.ControlEvent):
        self.reset()
        self.open = False
        self.update()
    
    def _handle_on_clean(self, event: ft.ControlEvent):
        self.reset()
        self._paternal_surname.focus()
        self.update()
    
    def _handle_on_save(self, event: ft.ControlEvent):
        customer = Customer(
            apellido_paterno=str(self._paternal_surname.value),
            apellido_materno=str(self._maternal_surname.value),
            nombres=str(self._customer_names.value),
            numero_de_cuenta=str(self._account_number.value)
        )
        accounts.add(customer)
        self.reset()
        self.close_form()
