# Telegram Expense Tracker 📅💸

Telegram-бот и веб-приложение для отслеживания личных расходов. Проект реализован на **Django** и использует **SQLite** для хранения данных.

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/kortex091/django_expense_bot.git
cd django_expense_bot
```

### 2. Запуск проекта с помощью Docker Compose

**1.** Убедитесь, что у вас установлен **Docker** и **Docker Compose**.

**2.** Запустите проект командой:

```bash
docker-compose up -d
```

Проект будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

### 3. Миграции базы данных

Выполните миграции внутри работающего контейнера:

```bash
docker-compose exec web python manage.py migrate
```

### 4. Запуск Telegram-бота

Чтобы запустить бота внутри контейнера:

```bash
docker-compose exec web python manage.py runbot
```

---

## 💡 Функциональность

- **/add** - Добавление нового расхода.
- **/list** - Просмотр всех расходов.
- **/del <id>** - Удаление расхода по ID.

## 📊 Веб-интерфейс

На странице `/expenses` доступна таблица со всеми расходами, добавленными через бота.

---

## 📝 Лицензия

Этот проект лицензирован под MIT License. См. [LICENSE](LICENSE) для подробностей.

---

🌟 **Автор:** [Bogdan](https://github.com/your-username)

Буду рад вашим вопросам и предложениям по улучшению! 😊
