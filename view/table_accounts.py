import flet as ft
from data.accounts import Accounts

def create_data_column(label: str, on_sort=None) -> ft.DataColumn:
    return ft.DataColumn(
        label=ft.Text(label),
        tooltip=f'Ordenar por {label.lower()}',
        on_sort=on_sort
    )

def create_data_row(cells: list[ft.DataCell]) -> ft.DataRow:
    return ft.DataRow(
        cells=cells,
    )

def create_snackbar(message: str) -> ft.SnackBar:
    return ft.SnackBar(
        content=ft.Row([ft.Text(message)], alignment=ft.MainAxisAlignment.CENTER),
    )

def show_message(event: ft.ControlEvent) -> None:
    account_num = event.control.content.value
    snackbar = create_snackbar(f'Número de cuenta copiado!')
    snackbar.open = True
    page: ft.Page = event.page
    page.overlay.append(snackbar)
    page.update()
    

def handle_on_click_cell(event: ft.ControlEvent) -> None:
    page: ft.Page = event.page
    page.set_clipboard(str(event.control.content.value))
    show_message(event)

# Ejecución 

accounts = Accounts()

table_account_colums: list[ft.DataColumn] = [
    create_data_column(
        label=column,
        on_sort=lambda e: print(e.control.data)
    ) for column in accounts.column_names
]

table_account_rows: list[ft.DataRow] = []
for index, row in accounts._df.iterrows():
    table_account_rows.append(
        create_data_row(
            cells=[
                ft.DataCell(ft.Text(row['Apellido Paterno'])),
                ft.DataCell(ft.Text(row['Apellido Materno'])),
                ft.DataCell(ft.Text(row['Nombres'])),
                ft.DataCell(ft.Text(row['Numero de Cuenta'], tooltip='Haz click para copiar el numero de cuenta')),
            ]
        )
    )

table = ft.DataTable(
    columns=table_account_colums,
    rows=table_account_rows
)
if table.rows:
    for row in table.rows:
        cell = row.cells[-1]
        cell.on_tap = handle_on_click_cell