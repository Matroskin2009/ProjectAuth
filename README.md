# ProjectAuth - Аутентификация с инвайт-системой

Система аутентификации с реферальной системой и инвайт-кодами. Космический неоновый дизайн.

## 🌟 Особенности

- Регистрация/авторизация по логину и паролю (имитация)
- Привязка номера телефона
- Генерация уникальных инвайт-кодов (6 символов)
- Система приглашений с отслеживанием рефералов
- Защита от повторной активации кодов
- Адаптивный космический дизайн
- Анимации и визуальные эффекты

## 🛠 Технологии

- Python 3.9+
- Django 3.2
- MariaDb
- HTML5/CSS3 (анимации на CSS)
- JavaScript (базовые AJAX-запросы)

## 🚀 Установка

1. Клонировать репозиторий:

git clone https://github.com/Matroskin2009/ProjectAuth.git
cd ProjectAuth
Создать и активировать виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Установить зависимости:

bash
pip install -r requirements.txt
Применить миграции:

bash
python manage.py migrate
Запустить сервер:

bash
python manage.py runserver
Использование
Перейдите по адресу http://127.0.0.1:8000/

Для регистрации введите: Логин, Пароль Номер телефона, После входа вы получите инвайт-код

В профиле можно:

Активировать чужой инвайт-код

Просматривать приглашенных пользователей

Структура проекта:
text
ProjectAuth/    
├── myapp/               # Основное приложение
│   ├── models.py        # Модели User и InviteActivation
│   ├── views.py         # Логика аутентификации и инвайтов
│   ├── templates/       # HTML-шаблоны
│   └── static/          # CSS/JS/изображения
├── manage.py            # Django CLI
└── requirements.txt     # Зависимости

