# ui/views/colors.py
import flet as ft
import re
from typing import List, Dict, Any, Optional
import asyncio


class ColorsView(ft.Container):
    """Страница с палитрой цветов Flet"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 10

        # Кэш для всех цветов
        self.all_colors_data: List[Dict[str, Any]] = []

        # Флаг для предотвращения многократной инициализации
        self._initialized = False
        self._loading = False

        # Инициализация UI без автоматической загрузки
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""

        # Поиск по цветам
        self.search_field = ft.TextField(
            label="Поиск цвета...",
            expand=True,
            on_change=self.filter_colors,
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=self.clear_search,
                icon_size=16,
                tooltip="Очистить поиск"
            ),
            on_submit=self.filter_colors,
            hint_text="Введите название или HEX-код",
            height=40,
        )

        # Переключатель тем
        self.theme_toggle = ft.Switch(
            label="Тёмный режим",
            value=False,
            on_change=self.toggle_background,
            tooltip="Переключить светлую/тёмную тему"
        )

        # Кнопка копирования всех цветов
        self.copy_all_btn = ft.ElevatedButton(
            "Копировать все",
            icon=ft.Icons.COPY_ALL,
            on_click=self.copy_all_colors,
            tooltip="Скопировать список всех цветов",
            height=40,
            style=ft.ButtonStyle(
                padding={ft.ControlState.DEFAULT: 8}
            )
        )

        # Сетка цветов
        self.colors_grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=100,
            child_aspect_ratio=0.5,
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
                                    ft.Text(
                                        "🎨 Палитра цветов Flet",
                                        size=24,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                ], expand=True),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(height=8),
                        ft.Row(
                            controls=[
                                self.search_field,
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
                    content=self.colors_grid,
                    padding=ft.padding.only(top=10),
                    expand=True,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0
        )

    def did_mount(self):
        """Вызывается после монтирования компонента"""
        if not self._initialized and self.page:
            self.page.run_task(self.load_colors_async)

    async def load_colors_async(self):
        """Асинхронная загрузка цветов"""
        if self._loading:
            return

        self._loading = True
        try:
            await self._load_colors_task()
        finally:
            self._loading = False
            self._initialized = True

    async def _load_colors_task(self):
        """Задача загрузки цветов"""
        # Получаем цвета
        colors_data = await self._get_colors_data()
        categorized = self._categorize_colors(colors_data)

        # Очищаем сетку
        self.colors_grid.controls.clear()
        self.all_colors_data.clear()

        # Заполняем сетку
        for category_name, colors in categorized.items():
            if not colors:
                continue

            # Заголовок категории
            self.colors_grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        category_name,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=(ft.Colors.GREY_300 if self.theme_toggle.value
                               else ft.Colors.GREY_700)
                    ),
                    padding=ft.padding.only(top=15, bottom=5, left=2),
                    col=7
                )
            )

            # Карточки цветов
            for color_data in colors:
                card = self._create_color_card(color_data)
                self.colors_grid.controls.append(card)
                self.all_colors_data.append(color_data)

        # Безопасное обновление только этого компонента
        self.update()

    async def _get_colors_data(self) -> List[Dict[str, Any]]:
        """Асинхронно получает данные цветов"""
        colors = []

        # Получаем всех членов перечисления ft.Colors
        for color_name, color_enum in ft.Colors.__members__.items():
            colors.append({
                'name': color_name,
                'value': color_enum.value,
                'object': color_enum,
                'display_value': f"ft.Colors.{color_name}"
            })

            # Даем возможность другим задачам работать
            await asyncio.sleep(0)

        return colors

    def _categorize_colors(self, colors_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Категоризирует цвета по типам"""
        categories = {
            "Основные цвета": [],
            "Material Design": [],
            "Системные цвета": [],
            "Оттенки серого": [],
            "Прочие": []
        }

        patterns = {
            "Основные цвета": [
                'RED', 'PINK', 'PURPLE', 'DEEP_PURPLE', 'INDIGO', 'BLUE',
                'LIGHT_BLUE', 'CYAN', 'TEAL', 'GREEN', 'LIGHT_GREEN', 'LIME',
                'YELLOW', 'AMBER', 'ORANGE', 'DEEP_ORANGE', 'BROWN', 'BLUE_GREY'
            ],
            "Оттенки серого": ['GREY', 'BLACK', 'WHITE']
        }

        for color in colors_data:
            name = color['name']

            if any(p in name for p in patterns["Основные цвета"]):
                categories["Основные цвета"].append(color)
            elif '_' in name and re.search(r'_\d+$', name):
                categories["Material Design"].append(color)
            elif any(p in name for p in patterns["Оттенки серого"]):
                categories["Оттенки серого"].append(color)
            elif re.search(r'(PRIMARY|SECONDARY|TERTIARY|ERROR|SURFACE|BACKGROUND|ON)', name):
                categories["Системные цвета"].append(color)
            else:
                categories["Прочие"].append(color)

        # Сортируем внутри категорий по имени
        for cat in categories:
            categories[cat].sort(key=lambda x: x['name'])

        return categories

    def _get_contrast_color_for_block(self, color_enum) -> ft.Colors:
        """Возвращает контрастный цвет (BLACK или WHITE) для заданного цвета."""
        color_name = color_enum.name

        # Светлые цвета (черный текст)
        if color_name in ['WHITE', 'TRANSPARENT']:
            return ft.Colors.BLACK

        # Цвета с суффиксами _50, _100, _200, _300, _400
        if re.search(r'_(50|100|200|300|400)$', color_name):
            return ft.Colors.BLACK

        # Некоторые основные светлые цвета
        if color_name in ['YELLOW', 'AMBER', 'LIME']:
            return ft.Colors.BLACK

        # Оттенки серого до 400
        if color_name.startswith('GREY_'):
            num_part = color_name.split('_')[1]
            if num_part.isdigit() and int(num_part) <= 400:
                return ft.Colors.BLACK

        # По умолчанию белый текст
        return ft.Colors.WHITE

    def _create_color_card(self, color_data: Dict[str, Any]) -> ft.Container:
        """Создаёт карточку для отображения цвета"""
        name = color_data['name']
        obj = color_data['object']
        display_value = color_data['display_value']

        # Контрастный цвет для иконки
        icon_color = self._get_contrast_color_for_block(obj)

        # Цвет для текста на фоне карточки
        text_color = ft.Colors.BLACK if not self.theme_toggle.value else ft.Colors.WHITE

        bg_color = ft.Colors.GREY_900 if self.theme_toggle.value else ft.Colors.WHITE

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Блок с цветом
                    ft.Container(
                        bgcolor=obj,
                        height=40,
                        expand=True,
                        on_click=lambda e: self._copy_color(display_value),
                        ink=True,
                        tooltip=f"Кликните чтобы скопировать\n{display_value}",
                        alignment=ft.alignment.center,
                        content=ft.Icon(
                            ft.Icons.CONTENT_COPY,
                            color=icon_color,
                            size=20,
                            opacity=0.4
                        )
                    ),
                    # Информация о цвете
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                name.replace('_', ' ').title(),
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=text_color,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], spacing=0, tight=True),
                        padding=ft.padding.all(2)
                    )
                ],
                spacing=1,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=bg_color,
            data=color_data
        )

    def _copy_color(self, color_value: str):
        """Копирует значение цвета в буфер обмена"""
        try:
            if self.page:
                self.page.set_clipboard(color_value)
                self._show_snackbar(f"Скопировано: {color_value}")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(color_value)
                    self._show_snackbar(f"Скопировано: {color_value}")
                except ImportError:
                    self._show_snackbar("Не удалось скопировать")
        except Exception as e:
            self._show_snackbar(f"Ошибка копирования: {str(e)}")

    def copy_all_colors(self, e):
        """Копирует список всех цветов в буфер обмена"""
        try:
            colors_text = "Палитра цветов Flet:\n\n"
            for color in self.all_colors_data:
                colors_text += f"{color['display_value']}  # {color['value']}\n"

            if self.page:
                self.page.set_clipboard(colors_text)
                self._show_snackbar("Все цвета скопированы!")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(colors_text)
                    self._show_snackbar("Все цвета скопированы!")
                except ImportError:
                    self._show_snackbar("pyperclip не установлен")
        except Exception as e:
            self._show_snackbar(f"Ошибка: {str(e)}")

    def filter_colors(self, e):
        """Фильтрует цвета по поисковому запросу"""
        query = self.search_field.value.lower().strip()

        for control in self.colors_grid.controls:
            if hasattr(control, 'data') and control.data:
                # Карточка цвета
                name = control.data['name'].lower()
                value = control.data['value'].lower()
                display_value = control.data['display_value'].lower()
                searchable = f"{name} {value} {display_value}".lower()

                control.visible = query in searchable
            else:
                # Заголовок категории
                control.visible = True

        self.update()

    def clear_search(self, e):
        """Очищает поле поиска"""
        self.search_field.value = ""
        self.filter_colors(e)

    def toggle_background(self, e):
        """Переключает тему фона"""
        bg = ft.Colors.GREY_900 if self.theme_toggle.value else ft.Colors.WHITE
        text_color = ft.Colors.GREY_300 if self.theme_toggle.value else ft.Colors.GREY_700

        for control in self.colors_grid.controls:
            if hasattr(control, 'bgcolor'):
                control.bgcolor = bg

            # Обновляем цвет текста в заголовках
            if hasattr(control, 'content'):
                content = control.content
                if isinstance(content, ft.Text) and hasattr(content, 'color'):
                    content.color = text_color
                elif hasattr(content, 'controls'):
                    for item in content.controls:
                        if isinstance(item, ft.Text) and hasattr(item, 'color'):
                            item.color = text_color

        self.update()

    def _show_snackbar(self, message: str):
        """Показывает SnackBar с сообщением"""
        if self.page:
            snackbar = ft.SnackBar(
                content=ft.Text(message, size=12),
                duration=2000,
            )
            self.page.snack_bar = snackbar
            snackbar.open = True
            if not self.page.disposed:
                self.page.update()
        else:
            print(f"[Snackbar] {message}")

    def get_color_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Поиск цвета по имени"""
        for color in self.all_colors_data:
            if color['name'].lower() == name.lower():
                return color
        return None