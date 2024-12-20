# Viva

**Viva** — это веб-приложение на базе Django, предназначенное для бронирования столиков в ресторане. Приложение предлагает удобный интерфейс для клиентов для бронирования столиков, 
а также предоставляет менеджерам инструменты для утверждения или отклонения бронирований. Администраторы имеют полный контроль над системой, включая управление пользователями и бронированиями.

## Содержание

- [Функции](#функции)
- [Технологический Стек](#технологический-стек)
- [Предварительные Требования](#предварительные-требования)
- [Установка](#установка)


## Функции

- **Аутентификация Пользователей:** Безопасная регистрация и вход для клиентов, менеджеров и администраторов.
- **Управление Столиками:** Администраторы могут добавлять, обновлять или удалять столики с разной вместимостью.
- **Система Бронирования:** Клиенты могут бронировать столики, выбирая доступные даты и время.
- **Панель Менеджера:** Менеджеры могут просматривать, утверждать или отклонять ожидающие бронирования.
- **Личный Кабинет:** Пользователи могут просматривать свои текущие и прошедшие бронирования, а также отменять предстоящие бронирования.
- **Ролевая Модель Доступа:** Различные функциональности доступны в зависимости от ролей пользователей (Клиент, Менеджер, Администратор).

## Технологический Стек

- **Backend:** Django 5.1.4
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **База Данных:** postgresql
- **Python:** 3.10.12
- **Другие Библиотеки:** Встроенные системы аутентификации и управления Django


### Описание Ключевых Компонентов

- **booking/**: Содержит основную функциональность, связанную с бронированием столиков.
  - **models.py**: Определяет модели `Table` и `Booking`.
  - **views.py**: Обрабатывает логику для профилей пользователей, панели менеджера, создания, подтверждения и отмены бронирований.
  - **forms.py**: Содержит формы для бронирования и взаимодействия с пользователем.
  - **templatetags/**: Пользовательские шаблонные теги для ролевого доступа в шаблонах.
  - **management/commands/**: Пользовательские команды управления Django, такие как создание начальных пользователей и групп.
  - **templates/booking/**: HTML-шаблоны, специфичные для приложения бронирования.

- **users/**: Управляет функциональностью, связанной с пользователями.
  - **models.py**: Модель пользователя (если применимо).
  - **views.py**: Обрабатывает регистрацию, вход и выход пользователей.
  - **templates/users/**: HTML-шаблоны для аутентификации пользователей.

- **viva/**: Директория конфигурации проекта.
  - **settings.py**: Настройки Django, включая установленные приложения, middleware, шаблоны, базы данных и т.д.
  - **urls.py**: Конфигурация URL проекта.

- **static/**: Содержит статические файлы, такие как CSS, JavaScript и изображения.
  - **booking/css/styles.css**: Пользовательские стили для приложения бронирования.


## Предварительные Требования

Перед началом убедитесь, что вы выполнили следующие требования:

- **Python 3.10.12** или выше, установленный на вашей системе.
- **pip** — пакетный менеджер Python.
- **Виртуальное Окружение** (опционально, но рекомендуется).

## Установка

### 1. Клонирование Репозитория

```bash
git clone https://github.com/LolopatIgor/viva_diplom
cd viva_diplom

2. Создание и Активация Виртуального Окружения

Рекомендуется использовать виртуальное окружение для управления зависимостями.

# Создание виртуального окружения с именем 'venv'
python3 -m venv venv

# Активация виртуального окружения
# На Windows:
venv\Scripts\activate

# На Unix или MacOS:
source venv/bin/activate

3. Установка Зависимостей

pip install --upgrade pip
pip install -r requirements.txt

Примечание: Убедитесь, что у вас есть файл requirements.txt, перечисляющий все необходимые пакеты. Если его нет, создайте его на основе потребностей вашего проекта, например:

Django==5.1.4

4. Применение Миграций

python manage.py migrate

5. Создание Начальных Пользователей и Групп

Выполните пользовательскую команду управления для создания администратора, менеджера и обычного пользователя, а также группы Manager и необходимых прав.

python manage.py csu

Настройка
Переменные Окружения

Создайте файл .env
Используйте шаблон .env.sample

После настройки примените миграции:

python manage.py migrate

Запуск Приложения

Запустите сервер разработки Django:

python manage.py runserver

Доступ к приложению будет доступен в браузере по адресу http://127.0.0.1:8000/.
Использование
Администратор

Администраторы имеют полный доступ к административной панели Django и могут управлять всеми аспектами приложения.

    Доступ к Админ-Панели:

    Перейдите по адресу http://127.0.0.1:8000/admin/ и войдите, используя учетные данные администратора, созданные с помощью команды управления (admin@gmail.com / 123).

    Управление Столиками и Бронированиями:
        Добавляйте, обновляйте или удаляйте столики.
        Просматривайте все бронирования и управляйте ролями пользователей.

Менеджер

Менеджеры могут утверждать или отклонять бронирования через панель менеджера.

    Вход как Менеджер:

    Используйте учетные данные менеджера (manager@gmail.com / 123) для входа.

    Доступ к Панели Менеджера:

    Нажмите на кнопку "Подтверждения бронирований" в навигационной панели или перейдите по адресу http://127.0.0.1:8000/booking/manager/.

    Утверждение или Отклонение Бронирований:
        Просматривайте ожидающие бронирования в таблице "Ожидающие бронирования".
        Утверждайте бронирования, нажав кнопку "Подтвердить".
        Отклоняйте бронирования, нажав кнопку "Отклонить".

Пользователь

Пользователи могут бронировать столики и управлять своими бронированиями.

    Регистрация или Вход:
        Зарегистрируйтесь под новой учетной записью или войдите, используя существующие учетные данные (user@gmail.com / 123).

    Бронирование Столика:
        Перейдите на страницу "Бронирование".
        Выберите столик, дату и время, а также укажите количество гостей.
        Отправьте запрос на бронирование.

    Управление Бронированиями:
        Доступ к "Личному Кабинету" для просмотра текущих и прошедших бронирований.
        Отмена предстоящих бронирований при необходимости.

Команды Управления
Создание Начальных Пользователей и Групп

Проект включает пользовательскую команду управления для создания начальных пользователей и группы Manager.

python manage.py csu

Функциональность:

    Создает администратора (admin@gmail.com / 123).
    Создает менеджера (manager@gmail.com / 123) и назначает его в группу Manager.
    Создает обычного пользователя (user@gmail.com / 123).



