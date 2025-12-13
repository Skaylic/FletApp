# ui/components/alerts.py
import flet as ft


class AlertDialog:
    def __init__(self, title: str = '', content: str = None, confirm_text: str = "OK"):
        self.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton(confirm_text, on_click=self.close_dialog)
            ],
        )
        self.page = None

    def open_dialog(self, page: ft.Page):
        self.page = page
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()

    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()