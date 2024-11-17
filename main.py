from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

print("Environment Variables:")
print(f"Bot Token: {TELEGRAM_BOT_TOKEN}")
print(f"Channel Username: {CHANNEL_USERNAME}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with channel link button when the command /start is issued."""
    keyboard = [
        [InlineKeyboardButton("Join Our Channel!", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Check Subscription", callback_data='check_subscription')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome! Please join our channel to access exclusive content.",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if user is subscribed to the channel."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    print(f"\nChecking subscription for user_id: {user_id}")
    print(f"Channel username being checked: {CHANNEL_USERNAME}")
    
    try:
        print("Attempting to check channel membership...")
        # Check user's membership in the channel
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        print(f"Member status retrieved: {member.status}")
        
        if member.status in ['member', 'administrator', 'creator']:
            print(f"User is a member with status: {member.status}")
            await query.message.edit_text(
                "Thank you for being a member of our channel! You now have access to all features."
            )
        else:
            print(f"User is not a member. Status: {member.status}")
            keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.edit_text(
                "Please join our channel to access exclusive content!",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error occurred while checking subscription: {str(e)}")
        print(f"Error type: {type(e)}")
        await query.message.edit_text(
            "An error occurred while checking your subscription. Please try again later."
        )

def main():
    """Start the bot."""
    # Create application
    print("\nAttempting to create bot application...")
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("Bot application created successfully!")
    except Exception as e:
        print(f"Error creating bot application: {str(e)}")
        return

    # Add handlers
    print("\nAdding handlers...")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription))
    print("Handlers added successfully!")

    # Start the bot
    print("\nStarting bot polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
