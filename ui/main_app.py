# ui/main_app.py
import flet as ft
from ui.views.dashboard import DashboardView
from ui.views.settings import SettingsView
from ui.layouts.appbar import CustomAppBar
from ui.layouts.sidebar import Sidebar
from ui.layouts.base import BaseLayout


class FletApp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        # Инициализация страницы
        self.setup_page()

        # Инициализация UI
        self.init_ui()

    def setup_page(self):
        self.page.title = "Flet App"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0
        # НЕ вызываем update здесь!

    def init_ui(self):
        self.sidebar = Sidebar(
            on_navigate_callback=self.on_navigate,
            initial_route="dashboard"
        )

        # Создаём представления
        self.views = {
            "dashboard": DashboardView(),
            "settings": SettingsView()
        }

        # Текущее активное представление
        self.current_view = self.views["dashboard"]

        # Создаём компоненты (передаём только page в appbar)
        self.appbar = CustomAppBar(self.page)
        # self.sidebar = Sidebar(self.on_navigate)

        # Создаём макет
        self.layout = BaseLayout(
            appbar=self.appbar,
            sidebar=self.sidebar,
            content=self.current_view,
            show_footer=True
        )

        # Устанавливаем контент
        self.content = self.layout

    def on_navigate(self, route: str):
        """Обработчик навигации"""
        if route in self.views:
            # Меняем контент в макете
            self.layout.content_area = self.views[route]