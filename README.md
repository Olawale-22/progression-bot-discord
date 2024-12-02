# Discord Progress Bot

A Discord bot that sends daily update requests to channel members and stores their responses in a Notion database.

## Features

- 🤖 Automated daily progress tracking
- 📝 Direct message interaction with users
- 📊 Notion database integration
- 📅 Dynamic date-based response tracking
- ⏰ 24-hour message scheduling

## Prerequisites

- Python 3.8+
- Discord Bot Token
- Notion Integration Token
- Notion Database with required structure

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd progression-bot
```

2. Create `.env` file:
```properties
DISCORD_BOT_TOKEN=your_discord_bot_token
CHANNEL_ID=your_channel_id
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id
```


3. Create virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install discord.py python-dotenv notion-client
```


## Notion Setup

1. Create a Notion integration at [Notion Developers](https://www.notion.so/my-integrations)
2. Create a database with columns:
   - `Pseudo` (Title column)
   - `Last Updated` (Date column)
3. Share database with integration
4. Copy database ID from URL

## Usage

1. Activate virtual environment:
```bash
.\.venv\Scripts\activate
```

2. Run the bot:
```bash
python bot.py
```

## Features

- **Daily Updates**: Bot automatically sends DMs to channel members
- **Response Tracking**: Stores responses in Notion database
- **Dynamic Columns**: Creates date-based columns for responses
- **User Management**: Tracks existing users and creates new entries

## Project Structure

```
discord-progress-bot/
├── .env                # Environment variables
├── .gitignore         # Git ignore file
├── bot.py             # Discord bot implementation
├── models.py          # Notion database interactions
└── README.md          # Project documentation
```

## Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token
- `CHANNEL_ID`: Target Discord channel ID
- `NOTION_TOKEN`: Notion integration token
- `NOTION_DATABASE_ID`: Notion database ID


## Demo

If everything works fine you get something these:
1. On the terminal for debug purposes, it prints out the number of users in the channel and their activity status with the bot
![Bot Activity Diagram](./readimg/Capture%20d’écran%20(5).png)
2. Notions Database
![Notion Database Diagram](./readimg/Capture%20d’écran%20(6).png)



## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request
