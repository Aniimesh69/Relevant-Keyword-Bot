import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import wordnet

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for the conversation
(
    INDUSTRY, OBJECTIVE, WEBSITE, SOCIAL_MEDIA, PPC_CAMPAIGN,
    AUDIENCE, LOCATION
) = range(7)

# Function to generate related keywords
def generate_related_keywords(keywords):
    related_keywords = set()
    for keyword in keywords:
        for synset in wordnet.synsets(keyword):
            for lemma in synset.lemmas():
                related_keywords.add(lemma.name().lower())
    return list(related_keywords)

# Function to fetch keywords from a URL
def fetch_keywords_from_url(url, keywords):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True).lower()
        words = re.findall(r'\b\w+\b', text_content)
        return [kw for kw in keywords if kw.lower() in words]
    except Exception as e:
        logger.error(f"Error parsing URL: {e}")
        return []

# Conversation handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Welcome to the Keyword Bot! Let's get started.\n"
        "What industry is your business in?"
    )
    return INDUSTRY

async def industry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['industry'] = update.message.text
    await update.message.reply_text("What is your business objective (e.g., lead generation, sales)?")
    return OBJECTIVE

async def objective(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['objective'] = update.message.text
    await update.message.reply_text("Do you have a website? If yes, please share the URL.")
    return WEBSITE

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    url = update.message.text
    if url.startswith("http"):
        context.user_data['website'] = url
    else:
        context.user_data['website'] = None
    await update.message.reply_text("Do you have any social media platforms? If yes, share the URL(s).")
    return SOCIAL_MEDIA

async def social_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['social_media'] = update.message.text
    await update.message.reply_text("Do you use PPC campaigns? (Yes/No)")
    return PPC_CAMPAIGN

async def ppc_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['ppc_campaign'] = update.message.text.lower() == "yes"
    await update.message.reply_text("Who are you trying to reach? (e.g., young adults, professionals, etc.)")
    return AUDIENCE

async def audience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['audience'] = update.message.text
    await update.message.reply_text("What location would you like to target?")
    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['location'] = update.message.text

    # Extract inputs
    industry = context.user_data.get('industry', '')
    objective = context.user_data.get('objective', '')
    website = context.user_data.get('website', '')

    # Generate keywords
    keywords = generate_related_keywords([industry, objective])
    if website:
        relevant_keywords = fetch_keywords_from_url(website, keywords)
    else:
        relevant_keywords = []

    # Respond to user
    await update.message.reply_text(
        f"Generated Keywords based on inputs:\n"
        f"Industry: {industry}\n"
        f"Objective: {objective}\n"
        f"Relevant Keywords: {', '.join(relevant_keywords) if relevant_keywords else 'No relevant keywords found.'}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled. Type /start to restart.")
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token("7506956825:AAE6gwBwQbYZx3rRMT6gE6cj3TLAQoJ_SdA").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INDUSTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, industry)],
            OBJECTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, objective)],
            WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, website)],
            SOCIAL_MEDIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, social_media)],
            PPC_CAMPAIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ppc_campaign)],
            AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, audience)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    import nltk
    nltk.download('wordnet')
    main()
