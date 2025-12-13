import flet as ft
from flet.core.alert_dialog import AlertDialog


class CustomAppBar(ft.Container):
    """
    Кастомная верхняя панель приложения (AppBar)

    Args:
        page: Ссылка на объект страницы Flet
        on_logout: Функция обратного вызова для обработки выхода
        on_notifications: Функция обратного вызова для обработки уведомлений
    """

    def __init__(self, page: ft.Page, on_logout=None, on_notifications=None):
        super().__init__()
        self.page = page

        # Основные настройки контейнера
        self.height = 60  # Высота панели
        self.bgcolor = ft.colors.BLUE  # Цвет фона

        # Горизонтальные отступы (в Flet 0.28.3 используем padding как число)
        self.padding = ft.Padding(20, 0, 20, 0)

        # Функции обратного вызова
        self.on_logout = on_logout
        self.on_notifications = on_notifications
        self.alert = AlertDialog(
            title=ft.Text(page.title),
            content=ft.Text("Test")
        )

        # Инициализация пользовательского интерфейса
        self.init_ui()

    def init_ui(self):
        """Инициализация элементов интерфейса AppBar"""

        # 1. КНОПКА ВЫХОДА
        logout_button = ft.IconButton(
            icon=ft.icons.LOGOUT,
            icon_color=ft.colors.WHITE,
            icon_size=24,
            tooltip="Выйти из системы",
            on_click=self._handle_logout,
        )

        # 2. КНОПКА УВЕДОМЛЕНИЙ
        notifications_button = ft.IconButton(
            icon=ft.icons.NOTIFICATIONS,
            icon_color=ft.colors.WHITE,
            icon_size=24,
            tooltip="Уведомления",
            on_click=self._handle_notifications,
        )

        # 3. ОСНОВНОЙ КОНТЕЙНЕР С ЭЛЕМЕНТАМИ
        self.content = ft.Row(
            controls=[
                # Иконка приложения
                ft.Icon(
                    ft.icons.APPS,
                    color=ft.colors.WHITE,
                    size=28,
                    tooltip="Главная",
                ),

                # Название приложения
                ft.Text(
                    "Flet Application",
                    size=24,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),

                # Растягиваемое пространство (для выравнивания кнопок справа)
                ft.Container(expand=True),

                # Кнопка уведомлений
                notifications_button,

                # Кнопка выхода
                logout_button,
            ],
            # Выравнивание элементов по левому краю
            alignment=ft.MainAxisAlignment.START,
            # Вертикальное выравнивание по центру
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,  # Расстояние между элементами
        )

    def _handle_logout(self, e: ft.ControlEvent):
        """
        Обработчик нажатия кнопки выхода

        Args:
            e: Событие клика
        """
        print("Logout clicked")

        # Если передан внешний обработчик, вызываем его
        if self.on_logout:
            self.on_logout(e)
        else:
            print("Logout clicked3")
            # Иначе показываем стандартное диалоговое окно
            self._show_logout_dialog()

    def _show_logout_dialog(self):
        """Показывает диалоговое окно выхода"""
        # Создаем диалоговое окно
        self.alert.title=ft.Text("Выход из системы"),
        self.alert.content=ft.Text("Вы уверены, что хотите выйти?"),
        self.alert.actions=[
                # Кнопка подтверждения выхода
                ft.TextButton(
                    "Да, выйти",
                    on_click=self._confirm_logout,
                    style=ft.ButtonStyle(color=ft.colors.RED)
                ),
                # Кнопка отмены
                ft.TextButton("Отмена", on_click=self._close_dialog)
            ],

        # Показываем диалоговое окно на странице
        self.alert.open = True,
        self.page.update()

    def _confirm_logout(self, e):
        """Обработчик подтверждения выхода"""
        print("Logout confirmed")

        # Закрываем диалоговое окно
        self._close_dialog(e)

        # Здесь можно добавить логику выхода из системы:
        # 1. Очистка сессии
        # 2. Перенаправление на страницу логина
        # 3. Оповещение сервера и т.д.

        # Пример простого уведомления после выхода
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Выход выполнен успешно"),
            duration=2000,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _handle_notifications(self, e: ft.ControlEvent):
        """
        Обработчик нажатия кнопки уведомлений

        Args:
            e: Событие клика
        """
        print("Notifications clicked")

        # Если передан внешний обработчик, вызываем его
        if self.on_notifications:
            self.on_notifications(e)
        else:
            # Иначе показываем стандартное диалоговое окно уведомлений
            self._show_notifications_dialog()

    def _show_notifications_dialog(self):
        """Показывает диалоговое окно с уведомлениями"""
        # Создаем диалоговое окно с уведомлениями
        dialog = ft.AlertDialog(
            title=ft.Text("Уведомления"),
            content=ft.Column(
                controls=[
                    # Пример уведомлений (можно заменить реальными данными)
                    self._create_notification_item(
                        "Новое сообщение",
                        "У вас новое сообщение от администратора",
                        ft.icons.MESSAGE,
                        "5 минут назад"
                    ),
                    self._create_notification_item(
                        "Обновление системы",
                        "Доступно обновление версии 2.0",
                        ft.icons.UPDATE,
                        "Вчера"
                    ),
                    self._create_notification_item(
                        "Задача завершена",
                        "Ваша задача 'Проект X' завершена",
                        ft.icons.CHECK_CIRCLE,
                        "2 дня назад"
                    ),
                ],
                spacing=10,
                height=200,
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=self._close_dialog),
                ft.TextButton("Очистить все",
                              on_click=self._clear_notifications,
                              style=ft.ButtonStyle(color=ft.colors.BLUE))
            ],
        )

        # Показываем диалоговое окно на странице
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _create_notification_item(self, title: str, message: str, icon: str, time: str):
        """
        Создает элемент уведомления для диалогового окна

        Args:
            title: Заголовок уведомления
            message: Текст уведомления
            icon: Иконка уведомления
            time: Время получения

        Returns:
            Container с элементом уведомления
        """
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=16, color=ft.colors.BLUE),
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text(time, size=11, color=ft.colors.GREY_600),
                ]),
                ft.Text(message, size=12, color=ft.colors.GREY_700),
            ]),
            padding=ft.padding.only(bottom=10),
        )

    def _clear_notifications(self, e):
        """Обработчик очистки всех уведомлений"""
        print("Notifications cleared")

        # Закрываем диалоговое окно
        self._close_dialog(e)

        # Показываем подтверждение очистки
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Все уведомления очищены"),
            duration=2000,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _close_dialog(self, e):
        """
        Закрывает активное диалоговое окно

        Args:
            e: Событие клика (не используется, но требуется Flet)
        """
        # Проверяем, есть ли активное диалоговое окно
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()