# ui/layouts/base.py
import flet as ft
from ui.layouts.footer import Footer


class BaseLayout(ft.Container):
    def __init__(self, appbar, sidebar, content, show_footer=True):
        super().__init__()
        self.expand = True
        self.appbar = appbar
        self.sidebar = sidebar
        self._content_area = content
        self.show_footer = show_footer

        self.init_ui()

    def init_ui(self):
        # Основной контейнер для контента
        self.content_container = ft.Container(
            content=self._content_area,
            expand=True
        )

        # Создаем основную структуру
        self.main_row = ft.Row(
            controls=[
                self.sidebar,
                ft.VerticalDivider(width=1),
                self.content_container,
            ],
            expand=True,
            spacing=0
        )

        # Создаем элементы макета
        layout_controls = [self.appbar, self.main_row]

        # Добавляем футер если нужно
        if self.show_footer:
            self.footer = Footer()
            layout_controls.append(self.footer)

        self.content = ft.Column(
            controls=layout_controls,
            spacing=0
        )

    @property
    def content_area(self):
        return self._content_area

    @content_area.setter
    def content_area(self, value):
        self._content_area = value
        # Обновляем контент в контейнере
        self.content_container.content = value
        self.update()