# ui/layouts/footer.py
import flet as ft
from datetime import datetime
import asyncio
from typing import Optional


class Footer(ft.Container):
    """Футер приложения с информацией о версии, дате и статусе подключения"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.height = 40
        self.bgcolor = ft.Colors.ON_INVERSE_SURFACE
        self.padding = ft.padding.symmetric(horizontal=20)
        self.alignment = ft.alignment.center

        # Статус подключения
        self._is_connected = True
        self._connection_last_check = datetime.now()

        # Асинхронные задачи
        self._update_time_task: Optional[asyncio.Task] = None
        self._check_task: Optional[asyncio.Task] = None
        self._monitor_task: Optional[asyncio.Task] = None

        # Ссылки на элементы UI
        self.connection_status_text: Optional[ft.Text] = None
        self.connection_status_dot: Optional[ft.Container] = None
        self.time_display_text: Optional[ft.Text] = None
        self.version_text: Optional[ft.Text] = None

        # Инициализация UI
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса футера"""
        current_year = datetime.now().year
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Индикатор статуса подключения
        self.connection_status_dot = ft.Container(
            width=10,
            height=10,
            border_radius=5,
            bgcolor=ft.Colors.GREEN_500,
            tooltip="Статус подключения\nКликните для проверки",
            on_click=self._manual_connection_check,
        )

        self.connection_status_text = ft.Text(
            value="Online",
            size=12,
            color=ft.Colors.GREEN_700,
            weight=ft.FontWeight.W_400,
            font_family="Roboto",
            no_wrap=True,
        )

        # Время и дата
        self.time_display_text = ft.Text(
            value=current_time,
            size=12,
            color=ft.Colors.ON_SURFACE_VARIANT,
            font_family="Roboto",
            no_wrap=True,
        )

        # Версия приложения
        self.version_text = ft.Text(
            value="v1.0.0",
            size=12,
            color=ft.Colors.ON_SURFACE_VARIANT,
            font_family="Roboto",
            no_wrap=True,
        )

        # Сборка интерфейса
        status_section = ft.Row(
            controls=[
                self.connection_status_dot,
                self.connection_status_text,
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        info_section = ft.Row(
            controls=[
                status_section,
                ft.VerticalDivider(
                    color=ft.Colors.OUTLINE,
                    width=1,
                    thickness=1,
                ),
                self.version_text,
                ft.VerticalDivider(
                    color=ft.Colors.OUTLINE,
                    width=1,
                    thickness=1,
                ),
                self.time_display_text,
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.content = ft.Row(
            controls=[
                # Левая часть: копирайт
                ft.Text(
                    f"© {current_year} Flet Application. Все права защищены.",
                    size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                    font_family="Roboto",
                    no_wrap=True,
                ),
                # Растягиваемый пробел
                ft.Container(expand=True),
                # Правая часть: статус, версия, время
                info_section,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def did_mount(self):
        """Вызывается после монтирования компонента"""
        # Запускаем обновление времени, если страница доступна
        if self.page:
            self.page.run_task(self.start_background_tasks)

    async def start_background_tasks(self):
        """Запуск фоновых задач"""
        # Запускаем обновление времени
        self._update_time_task = asyncio.create_task(self._update_time_loop())
        # Запускаем мониторинг подключения
        self._monitor_task = asyncio.create_task(self._connection_monitor_loop())

    async def _update_time_loop(self):
        """Цикл обновления времени"""
        while True:
            try:
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                if self.time_display_text:
                    self.time_display_text.value = current_time
                    if self.page:
                        self.page.update()
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Footer] Ошибка обновления времени: {e}")
                break

    async def _connection_monitor_loop(self):
        """Мониторинг подключения (имитация)"""
        import random

        while True:
            try:
                await asyncio.sleep(30)  # Проверка каждые 30 секунд

                # Имитация случайных сбоев подключения (10% вероятность)
                if random.random() < 0.1:
                    self.set_connection_status(False, "Соединение потеряно")
                    await asyncio.sleep(5)
                    self.set_connection_status(True, "Соединение восстановлено")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Footer] Ошибка мониторинга подключения: {e}")
                break

    def _manual_connection_check(self, e):
        """Ручная проверка подключения"""
        if self.page:
            self.page.run_task(self._async_manual_connection_check)

    async def _async_manual_connection_check(self):
        """Асинхронная ручная проверка подключения"""
        # Если уже идет проверка, не запускаем новую
        if self._check_task and not self._check_task.done():
            return

        # Показываем состояние проверки
        self._update_connection_ui(
            ft.Colors.YELLOW_500,
            "Проверка...",
            ft.Colors.YELLOW_700
        )

        try:
            # Создаем задачу проверки
            self._check_task = asyncio.create_task(self._perform_connection_check())
            await self._check_task
        except Exception as ex:
            print(f"[Footer] Ошибка проверки подключения: {ex}")
            self.set_connection_status(False, "Ошибка проверки")

    async def _perform_connection_check(self):
        """Выполнение проверки подключения"""
        try:
            # Имитация проверки сети (задержка 1-2 секунды)
            await asyncio.sleep(1.5)

            # В реальном приложении здесь была бы проверка сети
            # Для демонстрации всегда возвращаем успех
            self.set_connection_status(True, "Онлайн ✓")

        except Exception as ex:
            print(f"[Footer] Ошибка проверки подключения: {ex}")
            self.set_connection_status(False, "Ошибка проверки")

    def _update_connection_ui(self, dot_color, message, text_color):
        """Обновление UI статуса подключения"""
        if self.connection_status_dot:
            self.connection_status_dot.bgcolor = dot_color

        if self.connection_status_text:
            self.connection_status_text.value = message
            self.connection_status_text.color = text_color

        self._connection_last_check = datetime.now()

        if self.page:
            self.page.update()

    def set_connection_status(self, is_connected: bool, message: str = None):
        """
        Установить состояние подключения

        Args:
            is_connected: True — онлайн, False — офлайн
            message: Пользовательское сообщение (опционально)
        """
        self._is_connected = is_connected

        if is_connected:
            dot_color = ft.Colors.GREEN_500
            text_color = ft.Colors.GREEN_700
            default_message = "Онлайн"
        else:
            dot_color = ft.Colors.RED_500
            text_color = ft.Colors.RED_700
            default_message = "Офлайн"

        self._update_connection_ui(
            dot_color,
            message or default_message,
            text_color
        )

    def get_connection_status(self) -> bool:
        """
        Получить текущее состояние подключения

        Returns:
            bool: True если подключено, False если нет
        """
        return self._is_connected

    def get_last_check_time(self) -> datetime:
        """
        Получить время последней проверки подключения

        Returns:
            datetime: Время последней проверки
        """
        return self._connection_last_check

    def set_version(self, version: str):
        """
        Установить версию приложения

        Args:
            version: Строка версии (например, "v1.2.3")
        """
        if self.version_text:
            self.version_text.value = version
            if self.page:
                self.page.update()

    def get_version(self) -> str:
        """
        Получить текущую версию приложения

        Returns:
            str: Текущая версия
        """
        if self.version_text:
            return self.version_text.value
        return ""

    async def dispose(self):
        """Очистка ресурсов при удалении футера"""
        # Отменяем все задачи
        tasks_to_cancel = [
            self._update_time_task,
            self._monitor_task,
            self._check_task
        ]

        for task in tasks_to_cancel:
            if task and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        # Обнуляем ссылки на задачи
        self._update_time_task = None
        self._monitor_task = None
        self._check_task = None

    def will_unmount(self):
        """Вызывается перед удалением компонента"""
        # Запускаем очистку асинхронно
        if self.page:
            self.page.run_task(self.dispose)