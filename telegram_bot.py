import os
import asyncio
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Try to import telegram modules with fallback
TELEGRAM_AVAILABLE = False
try:
    from telegram import Update, Bot
    from telegram.ext import Application, CommandHandler, ContextTypes
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
    logger.info("Telegram modules imported successfully")
except ImportError as e:
    logger.warning(f"Telegram modules not available: {e}")

# Global bot instance
trucking_bot = None

def initialize_bot():
    """Initialize the bot instance"""
    global trucking_bot
    if not TELEGRAM_AVAILABLE:
        logger.warning("Telegram bot cannot be initialized - modules not available")
        return False
    
    try:
        trucking_bot = TruckingBot()
        logger.info("Telegram bot initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Telegram bot: {e}")
        return False

async def send_application_to_telegram(form_data, files):
    """Send application data to Telegram bot subscribers"""
    global trucking_bot
    if not TELEGRAM_AVAILABLE:
        logger.info("Telegram not available - skipping notification")
        return False
        
    if trucking_bot:
        try:
            await trucking_bot.send_application_to_subscribers(form_data, files)
            return True
        except Exception as e:
            logger.error(f"Error sending application to Telegram: {e}")
            return False
    else:
        logger.warning("Telegram bot not initialized")
        return False

def run_bot_polling():
    """Run the bot in polling mode (for development/testing)"""
    if not TELEGRAM_AVAILABLE:
        logger.error("Cannot run bot polling - Telegram modules not available")
        return
        
    global trucking_bot
    if not trucking_bot:
        initialize_bot()
    
    if trucking_bot:
        application = trucking_bot.setup_application()
        application.run_polling(allowed_updates=Update.ALL_TYPES)

# Only define TruckingBot class if telegram modules are available
if TELEGRAM_AVAILABLE:
    class TruckingBot:
        def __init__(self):
            self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if not self.bot_token:
                raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
            
            self.bot = Bot(token=self.bot_token)
            self.subscribers = set()  # Store subscriber chat IDs
            self.subscribers_file = 'subscribers.json'
            self.load_subscribers()
        
        def load_subscribers(self):
            """Load subscribers from file"""
            try:
                if os.path.exists(self.subscribers_file):
                    with open(self.subscribers_file, 'r') as f:
                        data = json.load(f)
                        self.subscribers = set(data.get('subscribers', []))
            except Exception as e:
                logger.error(f"Error loading subscribers: {e}")
                self.subscribers = set()
        
        def save_subscribers(self):
            """Save subscribers to file"""
            try:
                with open(self.subscribers_file, 'w') as f:
                    json.dump({'subscribers': list(self.subscribers)}, f)
            except Exception as e:
                logger.error(f"Error saving subscribers: {e}")
        
        async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command"""
            chat_id = update.effective_chat.id
            self.subscribers.add(chat_id)
            self.save_subscribers()
            
            welcome_message = """
🚛 Добро пожаловать в бота для водителей грузовиков!

Этот бот будет уведомлять вас о новых заявках от водителей.
Когда кто-то отправит документы через форму на сайте, вы получите:
- Личные данные заявителя
- Все прикрепленные документы

Команды:
/start - Подписаться на уведомления
/stop - Отписаться от уведомлений
/status - Проверить статус подписки
"""
            await update.message.reply_text(welcome_message)
        
        async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /stop command"""
            chat_id = update.effective_chat.id
            if chat_id in self.subscribers:
                self.subscribers.remove(chat_id)
                self.save_subscribers()
                await update.message.reply_text("❌ Вы отписались от уведомлений о новых заявках.")
            else:
                await update.message.reply_text("ℹ️ Вы не были подписаны на уведомления.")
        
        async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /status command"""
            chat_id = update.effective_chat.id
            if chat_id in self.subscribers:
                await update.message.reply_text("✅ Вы подписаны на уведомления о новых заявках.")
            else:
                await update.message.reply_text("❌ Вы не подписаны на уведомления. Используйте /start для подписки.")
        
        async def send_application_to_subscribers(self, form_data, files):
            """Send new application to all subscribers"""
            if not self.subscribers:
                logger.info("No subscribers to notify")
                return
            
            # Format the message
            message = f"""
🚛 **Новая заявка от водителя**

👤 **Личные данные:**
• Имя: {form_data.get('full_name', 'Не указано')}
• Телефон: {form_data.get('phone', 'Не указан')}
• Email: {form_data.get('email', 'Не указан')}

📄 **Документы прикреплены:**
{len(files)} файл(ов)

⏰ Время подачи: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
            
            # Document names mapping
            document_names = {
                'drivers_license': 'Водительское удостоверение CDL',
                'medical_certificate': 'Медицинская справка DOT',
                'social_security': 'Карточка социального страхования',
                'vehicle_registration': 'Регистрация транспортного средства',
                'insurance_certificate': 'Страховой сертификат',
                'ifta_permit': 'Разрешение IFTA',
                'mc_authority': 'MC Authority'
            }
            
            # Send to all subscribers
            for chat_id in self.subscribers.copy():
                try:
                    # Send the main message
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    
                    # Send each file
                    for file_key, file_obj in files.items():
                        if file_key in document_names:
                            try:
                                file_obj.seek(0)  # Reset file pointer
                                await self.bot.send_document(
                                    chat_id=chat_id,
                                    document=file_obj,
                                    caption=f"📄 {document_names[file_key]}"
                                )
                            except Exception as e:
                                logger.error(f"Error sending file {file_key} to {chat_id}: {e}")
                    
                except Exception as e:
                    logger.error(f"Error sending message to subscriber {chat_id}: {e}")
                    # Remove invalid chat IDs
                    if "blocked" in str(e).lower():
                        self.subscribers.discard(chat_id)
                        self.save_subscribers()
        
        def setup_application(self):
            """Setup the telegram application with handlers"""
            application = Application.builder().token(self.bot_token).build()
            
            # Add command handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("stop", self.stop_command))
            application.add_handler(CommandHandler("status", self.status_command))
            
            return application
else:
    # Create empty TruckingBot class when telegram is not available
    class TruckingBot:
        def __init__(self):
            raise ValueError("Telegram bot functionality is not available - python-telegram-bot package not properly installed")