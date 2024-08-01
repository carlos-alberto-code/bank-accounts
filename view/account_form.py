import flet as ft

class Form(ft.AlertDialog):

    def __init__(self, on_save=None):
        self._apellido_paterno = self._create_txt_field(
            label='Apellido Paterno', input_filter=ft.TextOnlyInputFilter(),
            autofocus=True
        )
        self._apellido_materno = self._create_txt_field(
            label='Apellido Materno', input_filter=ft.TextOnlyInputFilter(),
        )
        self._nombres = self._create_txt_field(
            label='Nombres', input_filter=ft.TextOnlyInputFilter(), # TODO: Permitir espacio en blanco
        )
        self._cuenta = self._create_txt_field(
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
                )
            ),
            actions=[
                ft.ElevatedButton(
                    text='Cancelar', icon=ft.icons.CANCEL,
                    style=btn_style,
                    on_click=self.handle_on_cancel
                ),
                ft.ElevatedButton(
                    text='Limpiar', icon=ft.icons.CLEANING_SERVICES_SHARP,
                    style=btn_style,
                    on_click=self.handle_on_clean
                ),
                ft.ElevatedButton(
                    text='Guardar', icon=ft.icons.SAVE_ALT,
                    style=btn_style,
                    on_click=on_save
                )
            ]
        )
    
    def handle_on_clean(self, event: ft.ControlEvent):
        self.restet()
        self._apellido_paterno.focus()
        self.update()
    
    def handle_on_cancel(self, event: ft.ControlEvent):
        self.restet()
        self.open = False
        self.update()
    
    def _create_txt_field(self, label: str, input_filter: ft.InputFilter, autofocus: bool = False):
        return ft.TextField(
            label=label,
            height=40,
            border_radius=10,
            text_size=13,
            prefix_icon=ft.icons.PERSON,
            input_filter=input_filter,
            autofocus=autofocus
        )
    
    def restet(self):
        self._apellido_paterno.value = ''
        self._apellido_materno.value = ''
        self._nombres.value = ''
        self._cuenta.value = ''
        