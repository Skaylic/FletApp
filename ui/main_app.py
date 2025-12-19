# ui/main_app.py
import flet as ft
import asyncio
from ui.views.dashboard import DashboardView
from ui.views.settings import SettingsView
from ui.views.colors import ColorsView
from ui.views.icons import IconsView
from ui.layouts.appbar import CustomAppBar
from ui.layouts.sidebar import Sidebar
from ui.layouts.footer import Footer


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
        """Настройка страницы"""
        self.page.title = "Flet App - Документация и UI компоненты"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window_width = 1200
        self.page.window_height = 800

    def init_ui(self):
        """Инициализация интерфейса"""

        # Создаём представления и передаём page
        self.views = {
            "dashboard": DashboardView(page=self.page),
            "settings": SettingsView(page=self.page),
            "colors": ColorsView(page=self.page),
            "icons": IconsView(page=self.page)
        }

        # Текущее активное представление
        self.current_view = self.views["dashboard"]

        # Создаём компоненты
        self.appbar = CustomAppBar(page=self.page)

        self.sidebar = Sidebar(
            page=self.page,
            on_navigate_callback=self.on_navigate,
            initial_route="dashboard"
        )

        # Создаём футер
        self.footer = Footer(page=self.page)

        # Создаём основной макет
        self.content = self.create_main_layout()

    def create_main_layout(self):
        """Создание основного макета приложения"""
        return ft.Column(
            controls=[
                # AppBar
                self.appbar,

                # Горизонтальный разделитель
                ft.Divider(height=1, color=ft.Colors.OUTLINE),

                # Основное содержимое (Sidebar + View)
                ft.Row(
                    controls=[
                        # Sidebar
                        self.sidebar,

                        # Вертикальный разделитель
                        ft.VerticalDivider(width=1, color=ft.Colors.OUTLINE),

                        # Контентная область с прокруткой
                        ft.Container(
                            content=self.current_view,
                            expand=True,
                            padding=10,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),

                # Футер
                self.footer,
            ],
            expand=True,
            spacing=0,
        )

    def on_navigate(self, route: str):
        """Обработчик навигации"""
        if route in self.views:
            # Обновляем активный маршрут в сайдбаре
            self.sidebar.set_active_route(route)

            # Создаем новый view
            old_view = self.current_view
            self.current_view = self.views[route]

            # Обновляем layout
            self.update_layout()

            # Обновляем заголовок окна в зависимости от маршрута
            self.update_window_title(route)

            # Если нужно, перезагружаем данные в view
            if hasattr(self.current_view, 'did_mount'):
                self.current_view.did_mount()

            # Если есть метод загрузки, вызываем его
            if hasattr(self.current_view, 'load_icons'):
                self.current_view.load_icons()
            elif hasattr(self.current_view, 'load_colors'):
                self.current_view.load_colors()

            # Обновляем страницу
            if self.page:
                self.page.update()
        else:
            # Показать страницу 404
            self.show_not_found_page()

    def update_layout(self):
        """Обновление основного layout"""
        # Находим контейнер контента в Row
        content_row = self.content.controls[2]  # Row с sidebar и content
        # content_row.controls[2] это Container с current_view
        content_row.controls[2].content = self.current_view

    def update_window_title(self, route: str):
        """Обновление заголовка окна в зависимости от маршрута"""
        titles = {
            "dashboard": "Панель управления",
            "settings": "Настройки",
            "colors": "Цвета Flet",
            "icons": "Иконки Flet"
        }

        title = titles.get(route, "Flet App")
        if self.page:
            self.page.title = f"Flet App - {title}"
            self.page.update()

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
        content_row = self.content.controls[2]
        content_row.controls[2].content = not_found_view

        if self.page:
            self.page.update()

        # Автоматический редирект через 3 секунды
        async def redirect_to_dashboard():
            await asyncio.sleep(3.0)
            self.on_navigate("dashboard")

        if self.page:
            self.page.run_task(redirect_to_dashboard)

    def did_mount(self):
        """Вызывается после монтирования компонента"""
        # Обновляем заголовок для текущего маршрута
        route = self.get_current_view_name()
        self.update_window_title(route)

        # Загружаем данные для текущего view
        if hasattr(self.current_view, 'load_icons'):
            self.current_view.load_icons()
        elif hasattr(self.current_view, 'load_colors'):
            self.current_view.load_colors()

    def will_unmount(self):
        """Очистка ресурсов при удалении компонента"""
        # Очищаем ресурсы футера
        if self.footer and self.page:
            # Проверяем, есть ли метод dispose в футере
            if hasattr(self.footer, 'dispose'):
                self.page.run_task(self.footer.dispose)
            # Или метод will_unmount
            elif hasattr(self.footer, 'will_unmount'):
                self.footer.will_unmount()

    def get_current_view_name(self) -> str:
        """Получить название текущего представления"""
        for name, view in self.views.items():
            if view == self.current_view:
                return name
        return "unknown"

    def refresh_current_view(self):
        """Обновить текущее представление"""
        if hasattr(self.current_view, 'load_icons'):
            self.current_view.load_icons()
        elif hasattr(self.current_view, 'load_colors'):
            self.current_view.load_colors()
        elif hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()

        if self.page:
            self.page.update()