import flet as ft


class AppTheme:
    @staticmethod
    def light_theme():
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.BLUE,
                secondary=ft.colors.GREEN,
            )
        )

    @staticmethod
    def dark_theme():
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.BLUE_200,
                secondary=ft.colors.GREEN_200,
            )
        )