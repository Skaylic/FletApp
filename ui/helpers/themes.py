# ui/helpers/themes.py
import flet as ft


class AppTheme:
    @staticmethod
    def light_theme():
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.BLUE,
                secondary=ft.Colors.GREEN,
            )
        )

    @staticmethod
    def dark_theme():
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.BLUE_200,
                secondary=ft.Colors.GREEN_200,
            )
        )