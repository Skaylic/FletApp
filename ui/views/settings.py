# ui/views/settings.py
import flet as ft


class SettingsView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.init_ui()

    def init_ui(self):
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            options=[
                ft.dropdown.Option("light", "Light"),
                ft.dropdown.Option("dark", "Dark"),
                ft.dropdown.Option("auto", "Auto"),
            ],
            value="light",
            width=200
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Row(
                    controls=[
                        self.theme_dropdown,
                        ft.Switch(label="Notifications", value=True),
                    ],
                    spacing=20
                ),
                ft.TextField(
                    label="Username",
                    value="admin",
                    width=300
                ),
                ft.ElevatedButton(
                    text="Save Settings",
                    icon=ft.icons.SAVE,
                    on_click=self.on_save
                )
            ]
        )

    def on_save(self, e):
        print("Settings saved!")