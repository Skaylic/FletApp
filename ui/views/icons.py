# ui/views/icons.py
import flet as ft
import asyncio
from typing import List, Dict, Any, Optional, Tuple


class IconsView(ft.Container):
    """Страница с иконками Flet"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 10

        # Данные
        self.all_icons_data: List[Dict[str, Any]] = []
        self.displayed_icons: List[Dict[str, Any]] = []
        self.categories: Dict[str, List[str]] = {}

        # Для debounce фильтрации
        self.filter_task: Optional[asyncio.Task] = None
        self.last_filter_text = ""

        # Пагинация
        self.current_page = 0
        self.page_size = 60
        self.is_loading = False

        # Фильтры
        self.current_category = "Все"
        self.current_search = ""

        # Инициализация UI
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""

        # Поиск с debounce
        self.search_field = ft.TextField(
            label="Поиск иконок...",
            expand=True,
            on_change=self.on_search_change,
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=self.clear_search,
                icon_size=16,
                tooltip="Очистить поиск"
            ),
            hint_text="Введите название иконки",
            height=40,
        )

        # Поиск по категориям
        self.category_dropdown = ft.Dropdown(
            label="Категория",
            width=200,
            options=[
                ft.dropdown.Option("Все"),
            ],
            value="Все",
            on_change=self.filter_by_category,
        )

        # Переключатель размера
        self.size_slider = ft.Slider(
            min=24,
            max=72,
            divisions=4,
            value=40,
            label="{value}px",
            on_change=self.change_icon_size,
            width=150,
        )

        # Информация о количестве
        self.stats_text = ft.Text("", size=12)

        # Заголовок страницы
        self.header_text = ft.Text(
            "🖼️ Иконки Flet",
            size=24,
            weight=ft.FontWeight.BOLD
        )

        # Сетка с виртуализацией
        self.icons_grid = ft.GridView(
            expand=True,
            runs_count=self.get_runs_count(),
            max_extent=120,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        # Кнопки пагинации
        self.page_text = ft.Text("Страница 1", size=12)
        self.pagination_row = ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_page,
                    disabled=True,
                    tooltip="Предыдущая страница"
                ),
                self.page_text,
                ft.IconButton(
                    ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_page,
                    tooltip="Следующая страница"
                ),
                ft.TextButton(
                    "Показать все",
                    on_click=self.show_all,
                    tooltip="Показать все иконки (может замедлить работу)"
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False,
        )

        # Индикатор загрузки
        self.loading_indicator = ft.ProgressRing(
            width=20,
            height=20,
            visible=False
        )

        # Собираем интерфейс
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row(
                            controls=[
                                ft.Column([
                                    self.header_text,
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
                                self.category_dropdown,
                                ft.Container(width=10),
                                ft.Column([
                                    ft.Text("Размер:", size=12),
                                    self.size_slider,
                                ], spacing=0),
                                ft.Container(width=10),
                                self.loading_indicator,
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
                    padding=ft.padding.only(top=10),
                    expand=True,
                ),
                self.pagination_row
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0
        )

        # Загружаем иконки
        self.load_icons()

    def get_runs_count(self) -> int:
        """Определяет количество колонок в зависимости от ширины экрана"""
        if not self.page or not self.page.width:
            return 6
        return max(3, min(8, int(self.page.width / 140)))

    def load_icons(self):
        """Загружает все иконки"""
        self.loading_indicator.visible = True
        if self.page:
            self.page.update()

        self.load_all_icons()

        # Обновляем статистику
        self.update_stats()

        self.loading_indicator.visible = False
        if self.page:
            self.page.update()

    def load_all_icons(self):
        """Загружает иконки из ft.Icons и категоризирует их"""
        self.all_icons_data.clear()
        self.categories.clear()

        # Определяем категории
        category_patterns = {
            "Навигация": ['ARROW', 'CHEVRON', 'NAVIGATE', 'BACK', 'FORWARD',
                          'UP', 'DOWN', 'LEFT', 'RIGHT', 'HOME', 'MENU'],
            "Действия": ['ADD', 'REMOVE', 'DELETE', 'EDIT', 'SAVE', 'CLOSE',
                         'CHECK', 'CANCEL', 'DOWNLOAD', 'UPLOAD', 'SHARE',
                         'PRINT', 'SEARCH', 'FILTER', 'SETTINGS'],
            "Социальные": ['PERSON', 'PEOPLE', 'GROUP', 'ACCOUNT', 'FACE',
                           'THUMB', 'LIKE', 'HEART', 'STAR', 'COMMENT'],
            "Файлы и папки": ['FILE', 'FOLDER', 'DOCUMENT', 'IMAGE', 'PHOTO',
                              'VIDEO', 'MUSIC', 'CLOUD'],
            "Уведомления": ['NOTIFICATION', 'ALARM', 'WARNING', 'ERROR',
                            'INFO', 'HELP'],
            "Коммуникации": ['MAIL', 'EMAIL', 'PHONE', 'MESSAGE', 'CHAT', 'CALL'],
            "Время": ['TIME', 'DATE', 'CALENDAR', 'CLOCK', 'TIMER', 'HISTORY'],
            "Карты и места": ['LOCATION', 'MAP', 'PLACE', 'NAVIGATE', 'DIRECTION'],
            "Разное": ['KEY', 'LOCK', 'UNLOCK', 'VISIBILITY', 'EYE', 'SORT',
                       'REFRESH', 'CODE', 'LINK', 'ATTACH', 'TAG', 'BOOKMARK',
                       'FLAG', 'PALETTE', 'COLOR', 'BRIGHTNESS', 'VOLUME',
                       'MIC', 'CAMERA', 'HEADPHONES', 'BATTERY', 'WIFI',
                       'NETWORK', 'BLUETOOTH', 'USB', 'HARDWARE', 'DEVICE',
                       'COMPUTER', 'PHONE', 'TABLET', 'TV', 'WATCH']
        }

        # Получаем все атрибуты ft.Icons
        for attr_name in dir(ft.Icons):
            if not attr_name.startswith('_') and attr_name.isupper():
                try:
                    icon_value = getattr(ft.Icons, attr_name)

                    # Определяем категорию
                    category = "Разное"
                    for cat_name, patterns in category_patterns.items():
                        if any(pattern in attr_name.upper() for pattern in patterns):
                            category = cat_name
                            break

                    # Добавляем в данные
                    icon_data = {
                        'name': attr_name,
                        'value': icon_value,
                        'display_name': attr_name.replace('_', ' ').title(),
                        'category': category
                    }

                    self.all_icons_data.append(icon_data)

                    # Добавляем в категорию
                    if category not in self.categories:
                        self.categories[category] = []
                    self.categories[category].append(attr_name)

                except:
                    continue

        # Сортируем по имени
        self.all_icons_data.sort(key=lambda x: x['name'])

        # Обновляем выпадающий список категорий
        self.update_category_dropdown()

        # Для начала показываем только первую страницу
        self.displayed_icons = self.all_icons_data.copy()
        self.load_page(0)

    def update_category_dropdown(self):
        """Обновляет список категорий в выпадающем меню"""
        # Очищаем старые опции
        self.category_dropdown.options = [
            ft.dropdown.Option("Все")
        ]

        # Добавляем категории в алфавитном порядке
        for category in sorted(self.categories.keys()):
            count = len(self.categories[category])
            self.category_dropdown.options.append(
                ft.dropdown.Option(f"{category} ({count})")
            )

    def load_page(self, page_num: int):
        """Загружает конкретную страницу"""
        # Обновляем количество колонок для адаптивной сетки
        self.icons_grid.runs_count = self.get_runs_count()

        self.current_page = page_num

        # Вычисляем какие иконки показывать
        if self.page_size > 0 and len(self.displayed_icons) > self.page_size:
            start_idx = page_num * self.page_size
            end_idx = min(start_idx + self.page_size, len(self.displayed_icons))
            page_icons = self.displayed_icons[start_idx:end_idx]

            # Показываем пагинацию
            self.pagination_row.visible = True

            # Обновляем текст пагинации
            total_pages = max(1, (len(self.displayed_icons) + self.page_size - 1) // self.page_size)
            self.page_text.value = f"Страница {page_num + 1} из {total_pages}"

            # Обновляем кнопки
            self.pagination_row.controls[0].disabled = (page_num == 0)
            self.pagination_row.controls[2].disabled = (page_num >= total_pages - 1)
        else:
            # Показываем все иконки
            page_icons = self.displayed_icons
            self.pagination_row.visible = False

        # Очищаем сетку
        self.icons_grid.controls.clear()

        # Добавляем иконки текущей страницы
        icon_size = int(self.size_slider.value)

        for icon_data in page_icons:
            card = self.create_icon_card(icon_data, icon_size)
            self.icons_grid.controls.append(card)

        if self.page:
            self.page.update()

    def create_icon_card(self, icon_data: Dict[str, Any], size: int = 40):
        """Создаёт карточку иконки"""
        name = icon_data['name']
        icon_value = icon_data['value']
        display_name = icon_data['display_name']
        category = icon_data.get('category', 'Разное')

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Иконка
                    ft.Container(
                        content=ft.Icon(
                            icon_value,
                            size=size,
                            color=ft.Colors.BLUE,
                        ),
                        alignment=ft.alignment.center,
                        height=size + 20,
                    ),
                    # Название
                    ft.Container(
                        content=ft.Text(
                            display_name,
                            size=10,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        padding=ft.padding.symmetric(horizontal=5, vertical=2),
                    ),
                    # Категория (маленькая метка)
                    ft.Container(
                        content=ft.Text(
                            category,
                            size=8,
                            color=ft.Colors.GREY,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        padding=ft.padding.only(top=2),
                    )
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            padding=5,
            on_click=lambda e: self.copy_icon(icon_data),
            data=icon_data,
            tooltip=f"Категория: {category}\nft.Icons.{name}",
            ink=True,
        )

    async def on_search_change(self, e):
        """Обработчик поиска с debounce"""
        self.current_search = self.search_field.value.strip().lower()

        # Показываем/скрываем кнопку очистки
        self.search_field.suffix.visible = bool(self.current_search)

        # Отменяем предыдущую задачу фильтрации
        if self.filter_task and not self.filter_task.done():
            self.filter_task.cancel()

        # Если строка пустая и категория "Все" - сразу загружаем оригинальные данные
        if not self.current_search and self.current_category == "Все":
            await self.load_original_icons()
            return

        # Создаем новую задачу с задержкой
        self.filter_task = asyncio.create_task(self.debounced_filter())

    async def debounced_filter(self):
        """Фильтрация с задержкой 300мс"""
        try:
            # Ждем 300мс перед фильтрацией
            await asyncio.sleep(0.3)

            # Показываем индикатор загрузки
            self.loading_indicator.visible = True
            if self.page:
                self.page.update()

            # Применяем фильтры
            self.apply_filters()

        except asyncio.CancelledError:
            # Задача была отменена
            pass
        finally:
            # Скрываем индикатор загрузки
            self.loading_indicator.visible = False
            if self.page:
                self.page.update()

    def apply_filters(self):
        """Применяет все активные фильтры (категория + поиск)"""
        # Начинаем со всех иконок
        filtered = self.all_icons_data.copy()

        # Фильтрация по категории
        if self.current_category != "Все":
            # Убираем счетчик из названия категории если есть
            category_name = self.current_category.split(" (")[0]
            filtered = [icon for icon in filtered if icon['category'] == category_name]

        # Фильтрация по тексту поиска
        if self.current_search:
            filtered = [
                icon for icon in filtered
                if self.current_search in icon['name'].lower() or
                   self.current_search in icon['display_name'].lower()
            ]

        self.displayed_icons = filtered
        self.current_page = 0
        self.load_page(0)
        self.update_stats()

    async def filter_by_category(self, e):
        """Фильтрация по выбранной категории"""
        self.current_category = self.category_dropdown.value or "Все"

        # Если категория "Все" и нет поиска - загружаем все иконки
        if self.current_category == "Все" and not self.current_search:
            await self.load_original_icons()
        else:
            # Применяем фильтры
            self.apply_filters()

    async def load_original_icons(self):
        """Загружает оригинальные иконки (без фильтрации)"""
        self.displayed_icons = self.all_icons_data.copy()
        self.current_category = "Все"
        self.category_dropdown.value = "Все"
        self.current_page = 0
        self.load_page(0)
        self.update_stats()

    async def clear_search(self, e):
        """Очистка поиска"""
        self.search_field.value = ""
        self.current_search = ""
        self.search_field.suffix.visible = False

        # Если категория "Все" - загружаем все иконки
        if self.current_category == "Все":
            await self.load_original_icons()
        else:
            # Применяем фильтры (только по категории)
            self.apply_filters()

    async def next_page(self, e):
        """Следующая страница"""
        if self.page_size > 0:
            total_pages = max(1, (len(self.displayed_icons) + self.page_size - 1) // self.page_size)
            if self.current_page < total_pages - 1:
                self.current_page += 1
                self.load_page(self.current_page)

    async def prev_page(self, e):
        """Предыдущая страница"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page(self.current_page)

    async def show_all(self, e):
        """Показать все иконки на одной странице"""
        self.page_size = 0
        self.load_page(0)

    def change_icon_size(self, e):
        """Изменение размера иконок"""
        self.load_page(self.current_page)

    def update_stats(self):
        """Обновление статистики"""
        total = len(self.all_icons_data)
        showing = len(self.displayed_icons)

        if showing == total:
            self.stats_text.value = f"Всего иконок: {total} | Категории: {len(self.categories)}"
        else:
            self.stats_text.value = f"Показано: {showing} из {total} | Категории: {len(self.categories)}"

        if self.page:
            self.page.update()

    def copy_icon(self, icon_data: Dict[str, Any]):
        """Копирует название иконки в буфер обмена"""
        try:
            copy_text = f"ft.Icons.{icon_data['name']}"
            if self.page:
                self.page.set_clipboard(copy_text)
                self.show_snackbar(f"Скопировано: {copy_text}")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(copy_text)
                    self.show_snackbar(f"Скопировано: {copy_text}")
                except ImportError:
                    self.show_snackbar("Не удалось скопировать")
        except Exception as e:
            self.show_snackbar(f"Ошибка: {str(e)}")

    def show_snackbar(self, message: str):
        """Показывает SnackBar с сообщением"""
        if self.page:
            snackbar = ft.SnackBar(
                content=ft.Text(message, size=12),
                duration=2000,
            )
            self.page.snack_bar = snackbar
            snackbar.open = True
            self.page.update()

    def did_mount(self):
        """Вызывается после монтирования компонента"""
        # Инициализируем видимость кнопки очистки
        self.search_field.suffix.visible = bool(self.search_field.value)

        # Подписываемся на изменение размера окна для адаптивной сетки
        if self.page:
            self.page.on_resize = self.on_window_resize

    def on_window_resize(self, e):
        """Обработчик изменения размера окна"""
        # Обновляем количество колонок
        old_runs_count = self.icons_grid.runs_count
        new_runs_count = self.get_runs_count()

        if old_runs_count != new_runs_count:
            self.icons_grid.runs_count = new_runs_count
            self.load_page(self.current_page)

    def will_unmount(self):
        """Очистка ресурсов"""
        if self.filter_task and not self.filter_task.done():
            self.filter_task.cancel()