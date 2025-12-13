# main.py
import flet as ft
from ui.main_app import FletApp

def main(page: ft.Page):
    # Просто создаем приложение и добавляем на страницу
    app = FletApp(page)
    page.add(app)

# Запуск приложения
ft.app(
    target=main,
    # view=ft.AppView.WEB_BROWSER,
    # port=50000
)