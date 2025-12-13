# ui/layouts/footer.py
import flet as ft
from datetime import datetime
import asyncio


class Footer(ft.Container):
    """Футер приложения с информацией о версии, дате и статусе подключения"""

    def __init__(self, page: ft.Page = None):
        super().__init__()
        self.page = page
        self.height = 40
        self.bgcolor = ft.colors.GREY_200
        self.padding = ft.padding.symmetric(horizontal=20)
        self.margin = ft.margin.only(top=10)

        # Ссылки на элементы интерфейса
        self.connection_status = ft.Ref[ft.Row]()
        self.connection_dot = ft.Ref[ft.Container]()
        self.connection_text = ft.Ref[ft.Text]()
        self.time_text = ft.Ref[ft.Text]()

        self._is_connected = True
        self._update_time_task: asyncio.Task | None = None
        self._check_task: asyncio.Task | None = None
        self._event_loop = None

        self.init_ui()

        # Пробуем получить event loop, если он запущен
        try:
            self._event_loop = asyncio.get_running_loop()
        except RuntimeError:
            self._event_loop = None

        if self.page and self._event_loop:
            asyncio.create_task(self.start_time_updater())

    def init_ui(self):
        """Инициализация интерфейса футера"""
        current_year = datetime.now().year
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.content = ft.Row(
            controls=[
                # Левая часть: копирайт
                ft.Text(
                    f"© {current_year} Flet Application. All rights reserved.",
                    size=12,
                    color=ft.colors.GREY_700,
                    font_family="Roboto",
                    no_wrap=True,
                ),

                # Растягиваемый пробел
                ft.Container(expand=True),

                # Правая часть: статус, версия, дата
                ft.Row(
                    controls=[
                        # Индикатор подключения
                        ft.Row(
                            ref=self.connection_status,
                            controls=[
                                ft.Container(
                                    ref=self.connection_dot,
                                    width=10,
                                    height=10,
                                    border_radius=5,
                                    bgcolor=ft.colors.GREEN_500,
                                    tooltip="Статус подключения",
                                    on_click=self._manual_connection_check_sync,
                                ),
                                ft.Text(
                                    ref=self.connection_text,
                                    value="Online",
                                    size=12,
                                    color=ft.colors.GREEN_700,
                                    weight=ft.FontWeight.W_400,
                                    font_family="Roboto",
                                    no_wrap=True,
                                )
                            ],
                            spacing=5,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),

                        ft.VerticalDivider(
                            color=ft.colors.GREY_400,
                            width=1,
                            thickness=1,
                        ),

                        ft.Text(
                            "v1.0.0",
                            size=12,
                            color=ft.colors.GREY_700,
                            font_family="Roboto",
                            no_wrap=True,
                        ),

                        ft.VerticalDivider(
                            color=ft.colors.GREY_400,
                            width=1,
                            thickness=1,
                        ),

                        ft.Text(
                            ref=self.time_text,
                            value=current_time,
                            size=12,
                            color=ft.colors.GREY_700,
                            font_family="Roboto",
                            no_wrap=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def start_time_updater(self):
        """Запускает обновление времени (каждую минуту)"""
        if self._update_time_task and not self._update_time_task.done():
            return  # Уже запущен

        async def update_time():
            while True:
                try:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    if self.time_text.current:
                        self.time_text.current.value = current_time
                        if self.page and self.page.visible:
                            self.page.update()
                    await asyncio.sleep(60)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"[Footer] Ошибка обновления времени: {e}")
                    break

        self._update_time_task = asyncio.create_task(update_time())

    def _manual_connection_check_sync(self, e):
        """Синхронная обертка для ручной проверки подключения"""
        if self.page:
            # Используем page.run_task для запуска асинхронной функции
            self.page.run_task(self._manual_connection_check, e)

    async def _manual_connection_check(self, e):
        """Ручная проверка подключения по клику"""
        if self._check_task and not self._check_task.done():
            return  # Уже выполняется проверка

        # Показываем состояние проверки
        self._set_connection_ui(
            ft.colors.YELLOW_500,
            "Checking...",
            ft.colors.YELLOW_700
        )

        async def simulate_check():
            try:
                await asyncio.sleep(1)  # Имитация задержки сети
                self.set_connection_status(True, "Online")
            except Exception as ex:
                print(f"[Footer] Ошибка проверки подключения: {ex}")
                self.set_connection_status(False, "Error")

        self._check_task = asyncio.create_task(simulate_check())

    def _set_connection_ui(self, dot_color, message, text_color):
        """Вспомогательный метод для обновления UI подключения"""
        if not (self.connection_dot.current and self.connection_text.current):
            return

        self.connection_dot.current.bgcolor = dot_color
        self.connection_text.current.value = message
        self.connection_text.current.color = text_color

        if self.page and self.page.visible:
            self.page.update()

    def set_connection_status(self, is_connected: bool, message: str | None = None):
        """
        Установить состояние подключения

        Args:
            is_connected: True — онлайн, False — офлайн
            message: Пользовательское сообщение (опционально)
        """
        self._is_connected = is_connected

        dot_color = ft.colors.GREEN_500 if is_connected else ft.colors.RED_500
        text_color = ft.colors.GREEN_700 if is_connected else ft.colors.RED_700
        default_message = "Online" if is_connected else "Offline"

        self._set_connection_ui(
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

    async def start_background_tasks(self):
        """Запустить фоновые задачи (вызывается после инициализации event loop)"""
        try:
            self._event_loop = asyncio.get_running_loop()
            await self.start_time_updater()
        except RuntimeError:
            # Event loop не запущен, задачи не запускаем
            pass

    async def dispose(self):
        """Очистка ресурсов при удалении футера"""
        if self._update_time_task:
            self._update_time_task.cancel()
            try:
                await self._update_time_task
            except asyncio.CancelledError:
                pass
            finally:
                self._update_time_task = None

        if self._check_task:
            self._check_task.cancel()
            try:
                await self._check_task
            except asyncio.CancelledError:
                pass
            finally:
                self._check_task = None