import flet as ft

searcher = ft.TextField(
    prefix_icon=ft.icons.SEARCH,
    label='Buscar usuario o cuenta',
    border_radius=10,
    width=400,
    height=40,
    text_size=13,
    label_style=ft.TextStyle(size=13),
)
restart_button = ft.IconButton(
    ft.icons.REFRESH, icon_size=20,
    tooltip='Actualizar',
)
add_button = ft.IconButton(
    ft.icons.ADD, icon_size=20,
    tooltip='Registrar',
)
delete_button = ft.IconButton(
    ft.icons.DELETE, icon_size=20,
    tooltip='Eliminar',
)
