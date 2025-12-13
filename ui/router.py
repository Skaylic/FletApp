import flet as ft


class Router:
    def __init__(self, page: ft.Page):
        self.page = page

    def go_to_route(self, route, app_instance):
        """Перейти по маршруту"""
        # Получаем текущий FletApp для обновления состояния
        from ui.main_app import FletApp

        if route == "/dashboard":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Дашборд"
        elif route == "/settings":
            from ui.views.settings import SettingsView
            content = SettingsView(self.page, app_instance.theme).get_content()
            title = "Настройки"
        elif route == "/account":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Профиль"
        elif route == "/maps":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Карты"
        elif route == "/calendar":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Календарь"
        elif route == "/charts":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Графики"
        elif route == "/messages":
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Сообщения"
        else:
            from ui.views.dashboard import DashboardView
            content = DashboardView(self.page, app_instance.theme).get_content()
            title = "Дашборд"

        # Показываем представление
        app_instance.show_view(content, title)