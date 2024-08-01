import flet as ft
from view.table_accounts import table

def handle_on_submit(event: ft.ControlEvent):
    banner.open = False
    event.page.update()

def handle_on_change(event: ft.ControlEvent):
    pass

def handle_on_blur(event: ft.ControlEvent):
    banner.open = False
    event.page.update()

searcher = ft.TextField(
    prefix_icon=ft.icons.SEARCH,
    label='Buscar usuario o cuenta',
    border_radius=12,
    height=40,
    text_size=13,
    label_style=ft.TextStyle(size=13),
    on_submit=handle_on_submit,
    on_change=handle_on_change,
    on_blur=handle_on_blur,
)

banner = ft.Banner(
    content=searcher,
    actions=[ft.Container()],
    elevation=20,
    margin=30,
)


def handle_on_searcher_button_click(event: ft.ControlEvent):
    page: ft.Page = event.page
    banner.open = True
    page.overlay.append(banner)
    page.update()
    searcher.value = ''
    searcher.focus()


search_button = ft.IconButton(
    ft.icons.SEARCH, icon_size=20,
    tooltip='Buscar',
    on_click=handle_on_searcher_button_click
)
edit_button = ft.IconButton(
    ft.icons.EDIT, icon_size=20,
    tooltip='Editar',
)
add_button = ft.IconButton(
    ft.icons.ADD, icon_size=20,
    tooltip='Registrar',
)
delete_button = ft.IconButton(
    ft.icons.DELETE, icon_size=20,
    tooltip='Eliminar',
)


shape_content = ft.Container(
    content=ft.ResponsiveRow(
        controls=[
            ft.Row(
                [ft.MenuBar(
                    [search_button, add_button, edit_button, delete_button]
                )],alignment=ft.MainAxisAlignment.CENTER,
            ),
            table
        ]
    )
)