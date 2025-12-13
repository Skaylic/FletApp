# ui/components/cards.py
import flet as ft

class InfoCard(ft.Container):
    def __init__(self, title: str, value: str, icon: str, color: str = ft.colors.BLUE):
        super().__init__()
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = f"{color}50"
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, color=color, size=24),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD)
            ],
            spacing=10
        )