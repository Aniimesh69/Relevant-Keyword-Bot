# Telegram Keyword Bot

## Overview
The Telegram Keyword Bot is a conversational bot designed to assist businesses in generating industry-specific trending and relevant keywords. By collecting essential information from users, it leverages the inputs to create a customized list of keywords that can be used for various business objectives like marketing, lead generation, or audience targeting.

## Features
- Collects user input about their business and objectives.
- Analyzes website and social media content to generate relevant keywords.
- Supports PPC campaign analysis (optional).
- Provides industry and audience-specific keyword suggestions.
- Easy-to-use, conversational interface.

## Prerequisites
To run this bot, ensure you have the following:
- Python 3.9+
- Telegram Bot API token
- Required Python libraries:
  - `python-telegram-bot`
  - `nltk`
  - `requests`
  - `beautifulsoup4`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-keyword-bot.git
   cd telegram-keyword-bot
   ```

2. Install the dependencies:
   ```bash
   pip install python-telegram-bot nltk requests beautifulsoup4
   ```

3. Download the NLTK WordNet dataset:
   ```python
   import nltk
   nltk.download('wordnet')
   ```

4. Replace the placeholder token in the script with your Telegram Bot API token:
   ```python
   application = ApplicationBuilder().token("YOUR_BOT_API_TOKEN").build()
   ```

## How to Run
1. Start the bot by running the script:
   ```bash
   python bot.py
   ```

2. Open Telegram and start a chat with your bot.

3. Use the `/start` command to initiate the conversation and follow the prompts.

## Usage Flow
1. **Industry Information**: The bot asks for the user's industry (e.g., Retail, Construction).
2. **Business Objective**: Users specify their goals, like lead generation or sales.
3. **Website Analysis** (optional): Users provide their website URL for keyword extraction.
4. **Social Media** (optional): Users share social media links for additional analysis.
5. **PPC Campaigns** (optional): Users specify if they want PPC campaign analysis.
6. **Audience Targeting**: Users describe their target audience.
7. **Location Targeting**: Users provide their preferred locations for targeting.
8. **Keyword Generation**: The bot processes the input and generates a list of relevant keywords.

## Code Explanation
### Main Components
1. **Keyword Generation**:
   - Uses WordNet to generate related keywords for the given inputs.
   - Extracts keywords from the provided website content using BeautifulSoup.

2. **Telegram Bot Framework**:
   - Uses `python-telegram-bot` to handle user interactions.
   - Implements a `ConversationHandler` to manage multi-step interactions.

3. **Fallbacks and Error Handling**:
   - Includes fallbacks for canceling the operation.
   - Handles website parsing errors gracefully.

### States in the Conversation
| State           | Description                                |
|------------------|--------------------------------------------|
| `INDUSTRY`      | Collects the user's industry.             |
| `OBJECTIVE`     | Collects the business objective.          |
| `WEBSITE`       | Collects the website URL (optional).      |
| `SOCIAL_MEDIA`  | Collects social media links (optional).   |
| `PPC_CAMPAIGN`  | Collects PPC campaign information.        |
| `AUDIENCE`      | Collects details about the target audience.|
| `LOCATION`      | Collects preferred target locations.      |

## Example Interaction
1. **Bot**: Welcome to the Keyword Bot! Let's get started. What industry is your business in?
   **User**: Retail
2. **Bot**: What is your business objective (e.g., lead generation, sales)?
   **User**: Lead generation
3. **Bot**: Do you have a website? If yes, please share the URL.
   **User**: https://example.com
4. **Bot**: Generated Keywords based on inputs:
   - Retail
   - Lead generation

## Contribution
Contributions are welcome! Please fork the repository, create a branch for your feature or bug fix, and submit a pull request.



