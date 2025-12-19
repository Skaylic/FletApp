import flet as ft
import re
from typing import List, Dict, Any, Optional


class IconsView(ft.Container):
    """Страница с библиотекой иконок Flet"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 10

        # Кэш для всех иконок
        self.all_icons_data: List[Dict[str, Any]] = []

        # Текущий размер иконок
        self.current_icon_size = 24

        # Инициализация UI
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""

        # Создаем подзаголовок как атрибут
        self.stats_text = ft.Text(
            "Загрузка иконок...",
            size=14,
            color=ft.Colors.GREY_600
        )

        # Поиск по иконкам
        self.search_field = ft.TextField(
            label="Поиск иконки...",
            expand=True,
            on_change=self.filter_icons,
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=self.clear_search,
                icon_size=16,
                tooltip="Очистить поиск"
            ),
            on_submit=self.filter_icons,
            hint_text="Введите название иконки",
            height=40,
        )

        # Переключатель тем
        self.theme_toggle = ft.Switch(
            label="Тёмный режим",
            value=False,
            on_change=self.toggle_background,
            tooltip="Переключить светлую/тёмную тему"
        )

        # Кнопка копирования всех иконок
        self.copy_all_btn = ft.ElevatedButton(
            "Копировать все",
            icon=ft.Icons.COPY_ALL,
            on_click=self.copy_all_icons,
            tooltip="Скопировать список всех иконок",
            height=40,
            style=ft.ButtonStyle(
                padding={ft.ControlState.DEFAULT: 8}
            )
        )

        # Слайдер для размера иконок
        self.size_slider = ft.Slider(
            min=16,
            max=48,
            divisions=8,
            value=24,
            label="{value}px",
            on_change=self.change_icon_size,
            expand=True,
        )

        # Сетка иконок
        self.icons_grid = ft.GridView(
            expand=True,
            runs_count=8,
            max_extent=100,
            child_aspect_ratio=0.8,
            spacing=4,
            run_spacing=4
        )

        # Основной контент
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row(
                            controls=[
                                ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.IMAGE_SEARCH, size=32,
                                                color=ft.Colors.BLUE),
                                        ft.Text(
                                            "Библиотека иконок Flet",
                                            size=24,
                                            weight=ft.FontWeight.BOLD
                                        )
                                    ], spacing=10),
                                    # Используем атрибут
                                    self.stats_text,
                                ], expand=True),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(height=8),
                        ft.Row(
                            controls=[
                                self.search_field,
                                ft.Container(width=10),
                                ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.ZOOM_IN, size=16),
                                        ft.Text("Размер:", size=12),
                                    ], spacing=5),
                                    self.size_slider,
                                ], tight=True),
                                ft.Container(width=10),
                                self.theme_toggle,
                                ft.Container(width=10),
                                self.copy_all_btn
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8
                        ),
                    ]),
                    padding=ft.padding.only(bottom=10)
                ),
                ft.Divider(height=1),
                ft.Container(
                    content=self.icons_grid,
                    expand=True,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0
        )

        # Загружаем иконки
        self.load_icons()

    def load_icons(self):
        """Загружает все иконки"""
        self.load_all_icons()

    def load_all_icons(self):
        """Загружает и категоризирует все иконки Flet"""
        self.all_icons_data.clear()
        self.icons_grid.controls.clear()

        icons_data = self.get_all_ft_icons()
        categorized = self.categorize_icons(icons_data)

        # Обновляем статистику в заголовке
        total_icons = len(icons_data)
        active_categories = len([c for c in categorized.values() if c])
        self.stats_text.value = f"{total_icons} иконок в {active_categories} категориях"

        for category_name, icons in categorized.items():
            if not icons:
                continue

            # Заголовок категории
            self.icons_grid.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            category_name,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=(ft.Colors.GREY_300 if self.theme_toggle.value
                                   else ft.Colors.GREY_700)
                        ),
                        ft.Text(
                            f"({len(icons)})",
                            size=12,
                            color=(ft.Colors.GREY_400 if self.theme_toggle.value
                                   else ft.Colors.GREY_500)
                        )
                    ], spacing=5),
                    padding=ft.padding.only(top=15, bottom=5, left=2),
                    col=8
                )
            )

            # Карточки иконок
            for icon_data in icons:
                card = self.create_icon_card(icon_data)
                self.icons_grid.controls.append(card)
                self.all_icons_data.append(icon_data)

        if self.page:
            self.page.update()

    def get_all_ft_icons(self) -> List[Dict[str, Any]]:
        """Получает все иконки из ft.Icons (Enum) через рефлексию"""
        icons = []

        try:
            # Получаем всех членов перечисления ft.Icons
            for icon_name, icon_enum in ft.Icons.__members__.items():
                # Пропускаем служебные
                if icon_name.startswith('_'):
                    continue

                try:
                    icons.append({
                        'name': icon_name,
                        'value': icon_enum.value,
                        'object': icon_enum,
                        'display_value': f"ft.Icons.{icon_name}",
                        'simple_value': f"Icons.{icon_name}"
                    })
                except:
                    continue
        except Exception as e:
            print(f"Ошибка при получении иконок: {e}")
            return self.get_basic_icons()

        # Сортируем по имени
        icons.sort(key=lambda x: x['name'])
        return icons

    def get_basic_icons(self) -> List[Dict[str, Any]]:
        """Возвращает список основных иконок для тестирования"""
        basic_icons = [
            {'name': 'HOME', 'value': 'home', 'display_value': 'ft.Icons.HOME', 'simple_value': 'Icons.HOME'},
            {'name': 'SEARCH', 'value': 'search', 'display_value': 'ft.Icons.SEARCH', 'simple_value': 'Icons.SEARCH'},
            {'name': 'SETTINGS', 'value': 'settings', 'display_value': 'ft.Icons.SETTINGS',
             'simple_value': 'Icons.SETTINGS'},
            {'name': 'PERSON', 'value': 'person', 'display_value': 'ft.Icons.PERSON', 'simple_value': 'Icons.PERSON'},
            {'name': 'EMAIL', 'value': 'email', 'display_value': 'ft.Icons.EMAIL', 'simple_value': 'Icons.EMAIL'},
        ]

        for icon in basic_icons:
            try:
                icon['object'] = getattr(ft.Icons, icon['name'])
            except:
                icon['object'] = ft.Icons.CIRCLE

        return basic_icons

    def categorize_icons(self, icons_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Категоризирует иконки по типам"""
        categories = {
            "Навигация": [],
            "Действия": [],
            "Уведомления": [],
            "Файлы": [],
            "Связь": [],
            "Медиа": [],
            "Устройства": [],
            "Редактирование": [],
            "Социальные": [],
            "Прочие": []
        }

        patterns = {
            "Навигация": ['HOME', 'MENU', 'ARROW', 'NAVIGATION', 'BACK', 'FORWARD'],
            "Действия": ['ADD', 'REMOVE', 'DELETE', 'EDIT', 'SAVE', 'CANCEL', 'CHECK'],
            "Уведомления": ['NOTIFICATION', 'ALARM', 'WARNING', 'ERROR', 'INFO'],
            "Файлы": ['FILE', 'FOLDER', 'DOCUMENT', 'IMAGE', 'DOWNLOAD'],
            "Связь": ['PHONE', 'CALL', 'MESSAGE', 'MAIL', 'EMAIL', 'CHAT'],
            "Медиа": ['PLAY', 'PAUSE', 'STOP', 'VOLUME', 'MUSIC', 'VIDEO'],
            "Устройства": ['PHONE', 'TABLET', 'LAPTOP', 'DEVICE', 'SCREEN'],
            "Редактирование": ['EDIT', 'COPY', 'PASTE', 'CUT', 'UNDO', 'FORMAT'],
            "Социальные": ['PERSON', 'ACCOUNT', 'GROUP', 'SHARE', 'LIKE', 'HEART'],
        }

        for icon in icons_data:
            name = icon['name'].upper()
            category_found = False

            for category, pattern_list in patterns.items():
                if any(pattern in name for pattern in pattern_list):
                    categories[category].append(icon)
                    category_found = True
                    break

            if not category_found:
                categories["Прочие"].append(icon)

        for cat in categories:
            categories[cat].sort(key=lambda x: x['name'])

        return categories

    def create_icon_card(self, icon_data: Dict[str, Any]) -> ft.Container:
        """Создаёт карточку для отображения иконки"""
        name = icon_data['name']
        obj = icon_data['object']
        display_value = icon_data['display_value']
        simple_value = icon_data.get('simple_value', display_value)

        # Определяем цвет иконки
        icon_color = (ft.Colors.BLUE_700 if not self.theme_toggle.value
                      else ft.Colors.BLUE_200)

        # Цвет для текста
        text_color = ft.Colors.BLACK if not self.theme_toggle.value else ft.Colors.WHITE

        # Фон карточки
        bg_color = (ft.Colors.GREY_50 if not self.theme_toggle.value
                    else ft.Colors.GREY_900)

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Блок с иконкой
                    ft.Container(
                        content=ft.Icon(
                            obj,
                            size=self.current_icon_size,
                            color=icon_color,
                        ),
                        height=50,
                        width=50,
                        alignment=ft.alignment.center,
                        on_click=lambda e: self.copy_icon(display_value),
                        ink=True,
                        tooltip=f"Нажмите для копирования\n{display_value}",
                        border_radius=8,
                        bgcolor=(ft.Colors.GREY_100 if not self.theme_toggle.value
                                 else ft.Colors.GREY_800),
                    ),
                    # Информация об иконке
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                name.replace('_', ' ').title(),
                                size=8,
                                weight=ft.FontWeight.BOLD,
                                color=text_color,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], spacing=0, tight=True),
                        padding=ft.padding.all(2)
                    )
                ],
                spacing=2,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=bg_color,
            border=ft.border.all(
                1,
                ft.Colors.GREY_300 if not self.theme_toggle.value
                else ft.Colors.GREY_700
            ),
            border_radius=8,
            padding=6,
            data=icon_data
        )

    def copy_icon(self, icon_value: str):
        """Копирует значение иконки в буфер обмена"""
        try:
            if self.page:
                self.page.set_clipboard(icon_value)
                self.show_snackbar(f"Скопировано: {icon_value}")
        except Exception as ex:
            self.show_snackbar(f"Ошибка копирования: {str(ex)}")

    def copy_all_icons(self, e):
        """Копирует список всех иконок в буфер обмена"""
        try:
            icons_text = "Библиотека иконок Flet:\n\n"
            for icon in self.all_icons_data:
                icons_text += f"{icon['display_value']}\n"

            if self.page:
                self.page.set_clipboard(icons_text)
                self.show_snackbar("Все иконки скопированы!")
        except Exception as e:
            self.show_snackbar(f"Ошибка: {str(e)}")

    def filter_icons(self, e):
        """Фильтрует иконки по поисковому запросу"""
        query = self.search_field.value.lower().strip()

        for control in self.icons_grid.controls:
            if hasattr(control, 'data') and control.data:
                # Карточка иконки
                name = control.data['name'].lower()
                value = control.data['value'].lower()
                display_value = control.data['display_value'].lower()
                simple_value = control.data.get('simple_value', '').lower()
                searchable = f"{name} {value} {display_value} {simple_value}".lower()

                control.visible = query in searchable
            else:
                # Заголовок категории
                control.visible = True

        if self.page:
            self.page.update()

    def clear_search(self, e):
        """Очищает поле поиска"""
        self.search_field.value = ""
        self.filter_icons(e)

    def change_icon_size(self, e):
        """Изменяет размер иконок"""
        self.current_icon_size = int(self.size_slider.value)

        for control in self.icons_grid.controls:
            if hasattr(control, 'data') and control.data:
                icon_container = control.content.controls[0]
                if hasattr(icon_container, 'content') and isinstance(icon_container.content, ft.Icon):
                    icon_container.content.size = self.current_icon_size

        if self.page:
            self.page.update()

    def toggle_background(self, e):
        """Переключает тему фона"""
        bg = ft.Colors.GREY_900 if self.theme_toggle.value else ft.Colors.WHITE
        border_color = ft.Colors.GREY_700 if self.theme_toggle.value else ft.Colors.GREY_300
        text_color = ft.Colors.GREY_300 if self.theme_toggle.value else ft.Colors.GREY_700

        for control in self.icons_grid.controls:
            if hasattr(control, 'bgcolor'):
                control.bgcolor = bg
                if hasattr(control, 'border'):
                    control.border = ft.border.all(1, border_color)

            if hasattr(control, 'content'):
                content = control.content
                if isinstance(content, ft.Text) and hasattr(content, 'color'):
                    content.color = text_color
                elif hasattr(content, 'controls'):
                    for item in content.controls:
                        if isinstance(item, ft.Text) and hasattr(item, 'color'):
                            item.color = text_color

        if self.page:
            self.page.update()

    def show_snackbar(self, message: str):
        """Показывает SnackBar с сообщением"""
        if self.page:
            snackbar = ft.SnackBar(
                content=ft.Text(message, size=12),
                duration=2000,
                bgcolor=ft.Colors.GREY_800 if self.theme_toggle.value else ft.Colors.GREY_200,
            )
            self.page.snack_bar = snackbar
            snackbar.open = True
            self.page.update()
        else:
            print(f"[Snackbar] {message}")

    # --- ДОПОЛНИТЕЛЬНЫЕ УЛУЧШЕНИЯ ---

    def on_resize(self, e):
        """Обрабатывает изменение размера окна"""
        if self.page and self.page.width:
            if self.page.width < 500:
                cols = 4
            elif self.page.width < 700:
                cols = 5
            elif self.page.width < 900:
                cols = 6
            elif self.page.width < 1100:
                cols = 7
            else:
                cols = 8
            self.icons_grid.runs_count = cols
            self.page.update()

    def init_event_listeners(self):
        """Подключает обработчики событий"""
        if self.page:
            self.page.on_resize = self.on_resize

    def did_mount(self):
        """Вызывается после монтирования компонента"""
        self.init_event_listeners()

    def will_unmount(self):
        """Вызывается перед удалением компонента"""
        pass

    def get_icon_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Поиск иконки по имени"""
        for icon in self.all_icons_data:
            if icon['name'].lower() == name.lower():
                return icon
        return None