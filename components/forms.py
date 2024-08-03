import flet as ft
from data.accounts_manager import AccountsManager

accounts = AccountsManager()

def create_txt_field(label: str, input_filter: ft.InputFilter, autofocus: bool = False, visible: bool = True) -> ft.TextField:
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

class NewCustomerForm(ft.AlertDialog):

    def __init__(self):
        self._apellido_paterno = create_txt_field(
            label='Apellido Paterno', input_filter=ft.TextOnlyInputFilter(),
            autofocus=True
        )
        self._apellido_materno = create_txt_field(
            label='Apellido Materno', input_filter=ft.TextOnlyInputFilter(),
        )
        self._nombres = create_txt_field(
            label='Nombres', input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]+$')
        )
        self._cuenta = create_txt_field(
            label='Número de cuenta', input_filter=ft.NumbersOnlyInputFilter()
        )
        btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        super().__init__(
            title=ft.Row([ft.Text('Nuevo cliente')], alignment=ft.MainAxisAlignment.CENTER),
            content=ft.Container(
                ft.Column(
                    [
                        ft.Divider(),
                        self._apellido_paterno,
                        self._apellido_materno,
                        self._nombres,
                        self._cuenta
                    ],
                    height=250
                )
            ),
            actions=[
                ft.ElevatedButton(
                    text='Cancelar', icon=ft.icons.CANCEL,
                    style=btn_style,
                    on_click=self._handle_on_cancel
                ),
                ft.ElevatedButton(
                    text='Limpiar', icon=ft.icons.CLEANING_SERVICES_SHARP,
                    style=btn_style,
                    on_click=self._handle_on_clean
                ),
                ft.ElevatedButton(
                    text='Guardar', icon=ft.icons.SAVE_ALT,
                    style=btn_style,
                    on_click=self._handle_on_save,
                )
            ]
        )
    
    def _handle_on_save(self, event: ft.ControlEvent):
        pass
    
    def _handle_on_clean(self, event: ft.ControlEvent):
        self.reset()
        self._apellido_paterno.focus()
        self.update()
    
    def _handle_on_cancel(self, event: ft.ControlEvent):
        self.reset()
        self.open = False
        self.update()
    
    def reset(self):
        self._apellido_paterno.value = ''
        self._apellido_materno.value = ''
        self._nombres.value = ''
        self._cuenta.value = ''


class EditCustomerForm(ft.AlertDialog):

    def __init__(self):
        self._account_txt_field = create_txt_field(
            label='Número de cuenta', input_filter=ft.NumbersOnlyInputFilter(),
            autofocus=True
        )
        self._button_search = ft.IconButton(
            icon=ft.icons.SEARCH,
            icon_size=20,
            on_click=self.handle_on_search_click
        )

        self._apellido_paterno = create_txt_field(
            label='Apellido Paterno', input_filter=ft.TextOnlyInputFilter(),
            autofocus=True,
            visible=False
        )
        self._apellido_materno = create_txt_field(
            label='Apellido Materno', input_filter=ft.TextOnlyInputFilter(),
            visible=False
        )
        self._nombres = create_txt_field(
            label='Nombres', input_filter=ft.InputFilter(regex_string=r'^[A-Za-z\s]+$'),
            visible=False
        )

        super().__init__(
            title=ft.Row([ft.Text('Editar cliente')], alignment=ft.MainAxisAlignment.CENTER),
            content=ft.Column(
                [
                    ft.Divider(),
                    ft.Row(
                        [self._account_txt_field, self._button_search],
                    ),
                    ft.Divider(),
                    self._apellido_paterno,
                    self._apellido_materno,
                    self._nombres
                ],
                width=350,
                height=70
            ),
            actions=[
                ft.ElevatedButton(
                    text='Cancelar', icon=ft.icons.CANCEL,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=self._handle_on_cancel
                ),
                ft.ElevatedButton(
                    text='Guardar', icon=ft.icons.SAVE_ALT,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    disabled=True,
                    on_click=self._handle_on_save
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
    
    def _handle_on_save(self, event: ft.ControlEvent):
        pass

    def handle_on_search_click(self, event: ft.ControlEvent):
        text = str(self._account_txt_field.value)
        self.show_search_result(text)

    def _handle_on_cancel(self, event: ft.ControlEvent):
        self.reset()
        self.open = False
        self.update()
    
    def reset(self):
        self._account_txt_field.value = ''
        self._apellido_paterno.value = ''
        self._apellido_materno.value = ''
        self._nombres.value = ''
        self._account_txt_field.focus()
        self._apellido_paterno.visible = False
        self._apellido_materno.visible = False
        self._nombres.visible = False
        self.content.height = 70 # type: ignore
    
    def show_search_result(self, account_number: str):
        customer = accounts.get(account_number)
        self._apellido_paterno.visible = True
        self._apellido_materno.visible = True
        self._nombres.visible = True
        self._apellido_paterno.value = customer.apellido_paterno
        self._apellido_materno.value = customer.apellido_materno
        self._nombres.value = customer.nombres
        self.content.height = 250 # type: ignore
        self.update()