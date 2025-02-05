# expenses/management/commands/runbot.py
import asyncio
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async  # Импортируем sync_to_async для обертки ORM-запросов
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from expenses.models import Expense

class Command(BaseCommand):
    help = 'Запускает Telegram-бота для управления расходами'

    def handle(self, *args, **options):
        TOKEN = '7349044974:AAHDRNWkABPDr-Yx5xL_pV02WSkS9nlM_Zc'  # Замените на ваш реальный токен

        # Асинхронный обработчик команды /start
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text(
                "Привет! Я помогу тебе отслеживать расходы. Используй /add для добавления расхода и /list для просмотра."
            )

        # Асинхронный обработчик команды /add <сумма> <категория>
        async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            try:
                args = context.args
                if len(args) < 2:
                    await update.message.reply_text("Пожалуйста, используйте формат: /add <сумма> <категория>")
                    return

                amount = float(args[0])
                category = ' '.join(args[1:])
                # Выполняем создание записи через Django ORM в синхронном режиме, обернутом в sync_to_async
                await sync_to_async(Expense.objects.create)(category=category, amount=amount)
                await update.message.reply_text(f"Добавлен расход: {category} - {amount} ₽")
            except ValueError:
                await update.message.reply_text("Ошибка: убедитесь, что сумма указана в числовом формате.")
            except Exception as e:
                await update.message.reply_text(f"Произошла ошибка: {e}")

        async def delete_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                msg_args = context.args
                if len(msg_args) != 1:
                    await update.message.reply_text("Пожалуйста, используйте формат: /del <id>")
                    return

                record_id = int(msg_args[0])
                # Выполняем создание записи через Django ORM в синхронном режиме, обернутом в sync_to_async

                record = await sync_to_async(Expense.objects.get)(pk=record_id)
                await sync_to_async(record.delete)()

                await update.message.reply_text(f"Запись удалена.")
            except ValueError:
                await update.message.reply_text("Ошибка: убедитесь, что сумма указана в числовом формате.")
            except Exception as e:
                await update.message.reply_text(f"Произошла ошибка: {e}")

        # Асинхронный обработчик команды /list
        async def list_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            # Оборачиваем получение списка расходов в sync_to_async
            expenses = await sync_to_async(list)(Expense.objects.all().order_by('-id')[:10])
            if expenses:
                message = "Последние расходы:\n"
                for expense in expenses:
                    message += f"{expense.category}: {expense.amount} ₽ (id={expense.pk})\n"
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Расходов пока нет.")

        # Создаем приложение Telegram-бота с новым API
        application = ApplicationBuilder().token(TOKEN).build()

        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("add", add_expense))
        application.add_handler(CommandHandler("list", list_expenses))
        application.add_handler(CommandHandler("del", delete_expense))

        self.stdout.write("Бот успешно запущен и ожидает команды.")
        # Запускаем поллинг
        application.run_polling()
