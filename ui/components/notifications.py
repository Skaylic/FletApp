import flet as ft

def show_snackbar(message: str = '', show: bool = False):
    return ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=ft.colors.GREEN_800,
        elevation=10,
        margin=10,
        duration=3000,
        action="Закрыть",
        action_color=ft.colors.WHITE,
        open=show
    )
