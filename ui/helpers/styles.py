# ui/helpers/styles.py
import flet as ft

# Общие стили кнопок
BUTTON_STYLE = ft.ButtonStyle(
    padding=ft.Padding(20, 10, 20, 10),
    elevation=2,
    shape=ft.RoundedRectangleBorder(radius=8),
)

# Стили текста
TITLE_STYLE = ft.TextStyle(
    size=24,
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.PRIMARY,
)

LABEL_STYLE = ft.TextStyle(
    size=14,
    color=ft.Colors.ON_SURFACE_VARIANT,
)
