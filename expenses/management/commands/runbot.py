import httpx
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
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
        TOKEN = '7349044974:AAHDRNWkABPDr-Yx5xL_pV02WSkS9nlM_Zc'  

        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text(
                "Привет! Я помогу тебе отслеживать расходы. Используй /add для добавления расхода и /list для просмотра."
            )

        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text(
                "Бот выполняет следующие команды:\n\n" \
                "/add <сумма> <категория> - добавляет запись в базу (категория вводится ОБЯЗАТЕЛЬНО)\n\n" \
                "/del <id записи> - удаляет запись из базы (id можно получить с помощью команды /list)\n\n" \
                "/list - выводит последние записи\n\n" \
                "/cat - отправляет картинки котиков"
            )

        
        async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            try:
                args = context.args
                if len(args) < 2:
                    await update.message.reply_text("Пожалуйста, используйте формат: /add <сумма> <категория>")
                    return

                amount = float(args[0])
                category = ' '.join(args[1:])
                
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
                

                record = await sync_to_async(Expense.objects.get)(pk=record_id)
                await sync_to_async(record.delete)()

                await update.message.reply_text(f"Запись удалена.")
            except ValueError:
                await update.message.reply_text("Ошибка: убедитесь, что сумма указана в числовом формате.")
            except Exception as e:
                await update.message.reply_text(f"Произошла ошибка: {e}")

        
        async def list_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            
            expenses = await sync_to_async(list)(Expense.objects.all().order_by('-id')[:10])
            if expenses:
                message = "Последние расходы:\n"
                for expense in expenses:
                    message += f"{expense.category}: {expense.amount} ₽ (id={expense.pk})\n"
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Расходов пока нет.")

        async def secret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text("Клевер любит Мяту")

        async def random_cat_pic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.thecatapi.com/v1/images/search", timeout=30.0)
                    response.raise_for_status()

                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        image_url = data[0].get("url")
                        await update.message.reply_photo(photo=image_url)
                    else:
                        await update.message.reply_text("Не удалось получить фото котика.")

            except Exception as e:
                await update.message.reply_text(f"Произошла ошибка: {e}")

        
        application = ApplicationBuilder().token(TOKEN).build()

        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_cmd))
        application.add_handler(CommandHandler("add", add_expense))
        application.add_handler(CommandHandler("list", list_expenses))
        application.add_handler(CommandHandler("del", delete_expense))
        application.add_handler(CommandHandler("secret", secret))
        application.add_handler(CommandHandler("cat", random_cat_pic))

        self.stdout.write("Бот успешно запущен и ожидает команды.")
        
        application.run_polling()
