import flet as ft
from ui.components.cards import InfoCard


class DashboardView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.init_ui()

    def init_ui(self):
        # Используем компонент InfoCard если он определен
        try:
            sales_card = InfoCard(
                title="Sales",
                value="1,234",
                icon=ft.icons.SHOW_CHART,
                color=ft.colors.BLUE
            )
            users_card = InfoCard(
                title="Users",
                value="567",
                icon=ft.icons.PEOPLE,
                color=ft.colors.GREEN
            )
        except:
            # Fallback если компонент не доступен
            sales_card = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.SHOW_CHART, size=40),
                    ft.Text("Sales", size=20),
                    ft.Text("1,234", size=32, weight=ft.FontWeight.BOLD)
                ]),
                padding=20,
                bgcolor=ft.colors.BLUE_50,
                border_radius=10,
                expand=True
            )
            users_card = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.PEOPLE, size=40),
                    ft.Text("Users", size=20),
                    ft.Text("567", size=32, weight=ft.FontWeight.BOLD)
                ]),
                padding=20,
                bgcolor=ft.colors.GREEN_50,
                border_radius=10,
                expand=True
            )

        self.content = ft.Column(
            controls=[
                ft.Text("Dashboard", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Row(
                    controls=[
                        sales_card,
                        users_card,
                    ],
                    spacing=20
                ),
                ft.Divider(height=30),
                ft.Text("Recent Activity", size=24),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Name")),
                        ft.DataColumn(ft.Text("Status")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("1")),
                            ft.DataCell(ft.Text("John")),
                            ft.DataCell(ft.Text("Active")),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("2")),
                            ft.DataCell(ft.Text("Alice")),
                            ft.DataCell(ft.Text("Active")),
                        ]),
                    ]
                )
            ]
        )