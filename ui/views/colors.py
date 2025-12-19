# ui/views/colors.py
import flet as ft
import re
from typing import List, Dict, Any, Optional


class ColorsView(ft.Container):
    """Страница с палитрой цветов Flet"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 10  # Уменьшаем общий padding

        # Кэш для всех цветов
        self.all_colors_data: List[Dict[str, Any]] = []

        # Инициализация UI
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""

        # Поиск по цветам
        self.search_field = ft.TextField(
            label="Поиск цвета...",
            expand=True,  # Занимает доступное пространство
            on_change=self.filter_colors,
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=self.clear_search,
                icon_size=16,  # Уменьшаем иконку
                tooltip="Очистить поиск"
            ),
            on_submit=self.filter_colors,
            hint_text="Введите название или HEX-код",
            height=40,  # Фиксируем высоту
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
            height=40,  # Фиксируем высоту
            style=ft.ButtonStyle(
                padding={ft.ControlState.DEFAULT: 8}  # Уменьшаем padding
            )
        )

        # Сетка цветов - УВЕЛИЧИВАЕМ колонок для более плотного расположения
        self.colors_grid = ft.GridView(
            expand=True,
            runs_count=5,  # Увеличиваем количество колонок
            max_extent=100,  # Уменьшаем ширину карточки
            child_aspect_ratio=0.5,  # Делаем более приземистыми
            spacing=4,  # Минимальные отступы
            run_spacing=4
        )

        # Индикатор загрузки
        self.loading_indicator = ft.ProgressRing(
            width=20,
            height=20,
            visible=False
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
                                        size=24,  # Уменьшаем заголовок
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
                                ft.Container(width=10),  # Уменьшаем отступ
                                self.theme_toggle,
                                ft.Container(width=10),  # Уменьшаем отступ
                                self.copy_all_btn
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8  # Уменьшаем spacing
                        ),
                    ]),
                    padding=ft.padding.only(bottom=10)  # Уменьшаем padding
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
            spacing=0  # Убираем spacing между элементами
        )

        # Загружаем цвета
        self.load_colors()

    def load_colors(self):
        """Загружает все цвета с индикацией процесса"""
        self.loading_indicator.visible = True
        if self.page:
            self.page.update()

        self.load_all_colors()

        self.loading_indicator.visible = False
        if self.page:
            self.page.update()

    def load_all_colors(self):
        """Загружает и категоризирует все цвета Flet"""
        self.all_colors_data.clear()
        self.colors_grid.controls.clear()

        colors_data = self.get_all_ft_colors()
        categorized = self.categorize_colors(colors_data)

        for category_name, colors in categorized.items():
            if not colors:  # Пропускаем пустые категории
                continue

            # Заголовок категории - делаем компактнее
            self.colors_grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        category_name,
                        size=14,  # Уменьшаем шрифт
                        weight=ft.FontWeight.BOLD,
                        color=(ft.Colors.GREY_300 if self.theme_toggle.value
                               else ft.Colors.GREY_700)
                    ),
                    padding=ft.padding.only(top=15, bottom=5, left=2),  # Уменьшаем padding
                    col=7  # Занимает всю ширину
                )
            )

            # Карточки цветов
            for color_data in colors:
                card = self.create_color_card(color_data)
                self.colors_grid.controls.append(card)
                self.all_colors_data.append(color_data)

        if self.page:
            self.page.update()

    def get_all_ft_colors(self) -> List[Dict[str, Any]]:
        """Получает все цвета из ft.Colors (Enum) через рефлексию"""
        colors = []

        # Получаем всех членов перечисления ft.Colors
        for color_name, color_enum in ft.Colors.__members__.items():
            colors.append({
                'name': color_name,
                'value': color_enum.value,
                'object': color_enum,
                'display_value': f"ft.Colors.{color_name}"
            })

        return colors

    def categorize_colors(self, colors_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
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

    def get_contrast_color_for_block(self, color_enum) -> ft.Colors:
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

    def create_color_card(self, color_data: Dict[str, Any]) -> ft.Container:
        """Создаёт карточку для отображения цвета - МИНИМАЛЬНАЯ ВЫСОТА"""
        name = color_data['name']
        obj = color_data['object']
        display_value = color_data['display_value']

        # Контрастный цвет для иконки
        icon_color = self.get_contrast_color_for_block(obj)

        # Цвет для текста на фоне карточки
        text_color = ft.Colors.BLACK if not self.theme_toggle.value else ft.Colors.WHITE

        bg_color = ft.Colors.GREY_900 if self.theme_toggle.value else ft.Colors.WHITE

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Блок с цветом - МИНИМАЛЬНАЯ ВЫСОТА
                    ft.Container(
                        bgcolor=obj,
                        height=40,  # Минимальная высота цветного блока
                        expand=True,
                        on_click=lambda e: self.copy_color(display_value),
                        ink=True,
                        tooltip=f"Кликните чтобы скопировать\n{display_value}",
                        alignment=ft.alignment.center,
                        # Иконку делаем меньше и менее заметной
                        content=ft.Icon(
                            ft.Icons.CONTENT_COPY,
                            color=icon_color,
                            size=20,  # Маленькая иконка
                            opacity=0.4  # Почти прозрачная
                        )
                    ),
                    # Информация о цвете - КОМПАКТНАЯ
                    ft.Container(
                        content=ft.Column([
                            # Только название цвета, без значения
                            ft.Text(
                                name.replace('_', ' ').title(),
                                size=12,  # Очень маленький шрифт
                                weight=ft.FontWeight.BOLD,
                                color=text_color,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], spacing=0, tight=True),
                        padding=ft.padding.all(2)  # Минимальные отступы
                    )
                ],
                spacing=1,  # Минимальный spacing
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=bg_color,
            # Без границ и теней для максимальной компактности
            data=color_data
        )

    def copy_color(self, color_value: str):
        """Копирует значение цвета в буфер обмена"""
        try:
            if self.page:
                self.page.set_clipboard(color_value)
                self.show_snackbar(f"Скопировано: {color_value}")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(color_value)
                    self.show_snackbar(f"Скопировано: {color_value}")
                except ImportError:
                    self.show_snackbar("Не удалось скопировать")
        except Exception as e:
            self.show_snackbar(f"Ошибка копирования: {str(e)}")

    def copy_all_colors(self, e):
        """Копирует список всех цветов в буфер обмена"""
        try:
            colors_text = "Палитра цветов Flet:\n\n"
            for color in self.all_colors_data:
                colors_text += f"{color['display_value']}  # {color['value']}\n"

            if self.page:
                self.page.set_clipboard(colors_text)
                self.show_snackbar("Все цвета скопированы!")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(colors_text)
                    self.show_snackbar("Все цвета скопированы!")
                except ImportError:
                    self.show_snackbar("pyperclip не установлен")
        except Exception as e:
            self.show_snackbar(f"Ошибка: {str(e)}")

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

        if self.page:
            self.page.update()

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

        if self.page:
            self.page.update()

    def show_snackbar(self, message: str):
        """Показывает SnackBar с сообщением"""
        if self.page:
            snackbar = ft.SnackBar(
                content=ft.Text(message, size=12),  # Уменьшаем шрифт
                duration=2000,  # Укорачиваем время показа
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
            # Адаптивное количество колонок
            if self.page.width < 600:
                cols = 4
            elif self.page.width < 900:
                cols = 5
            elif self.page.width < 1200:
                cols = 6
            else:
                cols = 7
            self.colors_grid.runs_count = cols
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

    def debug_print_colors(self):
        """Вывод всех цветов в консоль для отладки"""
        print("\n=== ВСЕ ЦВЕТА FLET ===")
        for color in self.all_colors_data:
            print(f"{color['display_value']} = {color['value']}")
        print(f"\nВсего цветов: {len(self.all_colors_data)}")

    def get_color_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Поиск цвета по имени"""
        for color in self.all_colors_data:
            if color['name'].lower() == name.lower():
                return color
        return None