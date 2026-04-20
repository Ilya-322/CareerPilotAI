# CareerPilot AI

**AI-powered Technical Interview Simulator**

Платформа для реалистичной подготовки к техническим собеседованиям с помощью искусственного интеллекта.

## О проекте

CareerPilot AI позволяет разработчикам проходить симуляции собеседований по следующим форматам:
- **Полное интервью**
- **Только Live-coding**
- **System Design**

Поддерживается выбор уровня сложности (Junior, Junior+, Middle) и стека технологий (Python).

## Основной функционал

- Создание симуляции с гибкими параметрами
- Динамическая подборка вопросов из базы данных
- Таймер и удобная навигация между вопросами
- Сохранение ответов пользователя
- Автоматический подсчёт результата и детальный разбор ответов
- Адаптивный современный интерфейс

## Технологический стек

- **Backend**: Python + Django
- **Frontend**: HTML + Tailwind CSS + JavaScript
- **База данных**: SQLite
- **Деплой**: PythonAnywhere

## Ссылки

- **Рабочая версия**: [https://ilyatem.pythonanywhere.com/](https://ilyatem.pythonanywhere.com/)
- **Тестовый аккаунт**:  
  **Email**: `test@careerpilot.ai`  
  **Пароль**: `Test12345`

## Как запустить локально

```bash
git clone https://github.com/Ilya-322/CareerPilotAI.git
cd CareerPilotAI

python -m venv venv
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
