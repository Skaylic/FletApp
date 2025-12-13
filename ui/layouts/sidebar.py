# ui/layouts/sidebar.py
import flet as ft


class Sidebar(ft.Container):
    """Боковая панель навигации с активными кнопками меню"""

    def __init__(self, on_navigate_callback, initial_route="dashboard"):
        """
        Инициализация Sidebar

        Args:
            on_navigate_callback: Функция обратного вызова при навигации
            initial_route: Начальный активный маршрут (по умолчанию "dashboard")
        """
        super().__init__()

        # Основные настройки контейнера
        self.width = 250  # Фиксированная ширина панели
        self.bgcolor = ft.colors.GREY_100  # Цвет фона
        self.padding = 0  # Без внутренних отступов

        # Состояние активного маршрута
        self.current_route = initial_route

        # Словарь для хранения ссылок на элементы меню
        self.menu_items = {}

        # Функция обратного вызова для навигации
        self.on_navigate = on_navigate_callback

        # Инициализация пользовательского интерфейса
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса панели"""

        # 1. ОСНОВНОЕ МЕНЮ
        main_menu = ft.Column(
            controls=[
                # Элементы навигации
                self._create_menu_item("Dashboard", ft.icons.DASHBOARD, "dashboard"),
                self._create_menu_item("Settings", ft.icons.SETTINGS, "settings"),
                self._create_menu_item("Analytics", ft.icons.ANALYTICS, "analytics"),
                self._create_menu_item("Documents", ft.icons.DESCRIPTION, "documents"),
            ],
            spacing=0,  # Без отступов между элементами
        )

        # 2. СЕКЦИЯ ВЫХОДА (внизу панели)
        logout_section = ft.Container(
            content=ft.Column(
                controls=[
                    # Разделитель
                    ft.Divider(color=ft.colors.GREY_300),
                    # Кнопка выхода
                    self._create_menu_item("Logout", ft.icons.LOGOUT, "logout", is_danger=True),
                ],
                spacing=0,
            ),
            padding=ft.padding.symmetric(vertical=10),  # Отступы сверху и снизу
        )

        # 4. ОСНОВНОЙ КОНТЕЙНЕР С КОЛОНОЧНОЙ СТРУКТУРОЙ
        self.content = ft.Column(
            controls=[
                # Основное меню (середина, растягивается)
                ft.Container(
                    content=main_menu,
                    padding=10,
                    expand=True,
                ),

                # Выход (низ)
                logout_section,
            ],
            spacing=0,  # Без отступов между секциями
            expand=True,  # Заполняет всё доступное пространство
        )

    def _create_menu_item(self, label: str, icon: str, route: str, is_danger: bool = False):
        """
        Создает элемент меню

        Args:
            label: Текст кнопки
            icon: Иконка из набора ft.icons
            route: Идентификатор маршрута
            is_danger: Флаг опасного действия (красный цвет)

        Returns:
            Контейнер с элементом меню
        """

        # Определяем, активен ли текущий элемент
        is_active = (route == self.current_route and route != "logout")

        # Создаем контейнер для элемента меню
        menu_container = ft.Container(
            # Содержимое: иконка + текст
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon,
                        color=self._get_icon_color(is_danger, is_active),
                        size=18,
                    ),
                    ft.Text(
                        label,
                        size=13,
                        weight=self._get_text_weight(is_active),
                        color=self._get_text_color(is_danger, is_active),
                    ),
                ],
                spacing=12,  # Расстояние между иконкой и текстом
            ),
            # Внутренние отступы
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            # Обработчик клика
            on_click=lambda e, r=route: self._handle_menu_click(r),
            # Визуальные стили
            bgcolor=self._get_bgcolor(is_active),
            border=self._get_border(is_active),
            ink=True,  # Эффект нажатия
        )

        # Сохраняем ссылку на созданный элемент для управления стилями
        self.menu_items[route] = {
            'container': menu_container,
            'icon': menu_container.content.controls[0],
            'text': menu_container.content.controls[1]
        }

        return menu_container

    def _handle_menu_click(self, route: str):
        """
        Обработчик клика по элементу меню

        Args:
            route: Идентификатор маршрута
        """
        # Запоминаем предыдущий активный маршрут
        old_route = self.current_route

        # Устанавливаем новый активный маршрут
        self.current_route = route

        # Обновляем визуальные стили кнопок
        self._update_active_state(old_route, route)

        # Вызываем функцию навигации
        self.on_navigate(route)

    def _update_active_state(self, old_route: str, new_route: str):
        """
        Обновляет визуальное состояние элементов меню

        Args:
            old_route: Предыдущий активный маршрут
            new_route: Новый активный маршрут
        """

        # 1. Сбрасываем стили для старого активного элемента
        if old_route in self.menu_items and old_route != "logout":
            item = self.menu_items[old_route]
            # Прозраный фон
            item['container'].bgcolor = ft.colors.TRANSPARENT
            # Убираем границу
            item['container'].border = None
            # Обычный цвет иконки и текста
            item['icon'].color = self._get_icon_color(False, False)
            item['text'].color = self._get_text_color(False, False)
            item['text'].weight = ft.FontWeight.NORMAL
            # Применяем изменения
            item['container'].update()

        # 2. Применяем активные стили для нового элемента (кроме logout)
        if new_route in self.menu_items and new_route != "logout":
            item = self.menu_items[new_route]
            # Синий фон
            item['container'].bgcolor = ft.colors.BLUE_50
            # Синяя граница
            item['container'].border = ft.border.all(1, ft.colors.BLUE_100)
            # Яркие цвета для активного состояния
            item['icon'].color = self._get_icon_color(False, True)
            item['text'].color = self._get_text_color(False, True)
            item['text'].weight = ft.FontWeight.BOLD
            # Применяем изменения
            item['container'].update()

    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ДЛЯ УПРАВЛЕНИЯ СТИЛЯМИ

    def _get_bgcolor(self, is_active: bool) -> ft.colors:
        """Возвращает цвет фона в зависимости от состояния"""
        return ft.colors.BLUE_50 if is_active else ft.colors.TRANSPARENT

    def _get_border(self, is_active: bool):
        """Возвращает границу в зависимости от состояния"""
        return ft.border.all(1, ft.colors.BLUE_100) if is_active else None

    def _get_text_color(self, is_danger: bool, is_active: bool) -> ft.colors:
        """Возвращает цвет текста"""
        if is_danger:
            return ft.colors.RED_600  # Красный для опасных действий
        elif is_active:
            return ft.colors.BLUE_700  # Синий для активного состояния
        return ft.colors.BLUE_GREY_800  # Серо-синий для обычного состояния

    def _get_icon_color(self, is_danger: bool, is_active: bool) -> ft.colors:
        """Возвращает цвет иконки"""
        if is_danger:
            return ft.colors.RED_600  # Красный для опасных действий
        elif is_active:
            return ft.colors.BLUE_600  # Синий для активного состояния
        return ft.colors.BLUE_GREY_700  # Серо-синий для обычного состояния

    def _get_text_weight(self, is_active: bool):
        """Возвращает толщину шрифта"""
        return ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL

    def set_active_route(self, route: str):
        """
        Устанавливает активный маршрут извне

        Args:
            route: Идентификатор маршрута для активации
        """
        old_route = self.current_route
        self.current_route = route
        self._update_active_state(old_route, route)