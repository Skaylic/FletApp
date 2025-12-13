# ui/main_app.py
import flet as ft
import threading
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

        # Создаём представления
        self.views = {
            "dashboard": DashboardView(),
            "settings": SettingsView()
        }

        # Текущее активное представление
        self.current_view = self.views["dashboard"]

        # Создаём компоненты (передаём только page в appbar)
        self.appbar = CustomAppBar(self.page)

        self.sidebar = Sidebar(
            on_navigate_callback=self.on_navigate,
            initial_route="dashboard"
        )

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
        """Обработчик навигации с плавной сменой контента"""
        if route in self.views:
            # Плавное скрытие текущего контента
            if hasattr(self.current_view, 'animate_opacity'):
                self.current_view.animate_opacity = 0
            else:
                self.current_view.opacity = 0

            self.page.update()

            # Смена контента
            self.current_view = self.views[route]
            self.layout.content_area = self.current_view

            # Плавное появление нового контента
            if hasattr(self.current_view, 'animate_opacity'):
                self.current_view.animate_opacity = 1
            else:
                self.current_view.opacity = 1

            # Обновление активной кнопки в сайдбаре
            self.sidebar.set_active_route(route)

            self.page.update()

        else:
            # Показать страницу 404 или вернуться на dashboard
            self.show_not_found_page()


    def show_not_found_page(self):
        """Страница 404 с автоматическим редиректом"""
        not_found_view = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=100, color=ft.Colors.RED_400),
                    ft.Text("Страница не найдена", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Через 3 секунды вы будете перенаправлены на главную страницу",
                            size=16, color=ft.Colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

        # Устанавливаем временную страницу
        self.layout.content_area = not_found_view
        self.page.update()

        # Автоматический редирект через 3 секунды
        def redirect_to_dashboard():
            self.on_navigate("dashboard")

        # Используем threading для задержки
        timer = threading.Timer(3.0, redirect_to_dashboard)
        timer.start()