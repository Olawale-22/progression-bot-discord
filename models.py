from notion_client import Client
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

# Add debug logging
print(f"Environment variables loaded: {list(os.environ.keys())}")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
print(f"NOTION_TOKEN value: {'Found' if NOTION_TOKEN else 'Missing'}")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def add_response_to_notion(user, response):
    # Format date for column name
    current_date = datetime.utcnow()
    date_column = current_date.strftime("Last Update %d/%m/%Y")
    
    # Search for existing user
    results = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "pseudo",
            "title": {
                "equals": user
            }
        }
    )

    # First, ensure the message column exists
    try:
        database = notion.databases.retrieve(database_id=DATABASE_ID)
        if date_column not in database['properties']:
            # Add new column if it doesn't exist
            notion.databases.update(
                database_id=DATABASE_ID,
                properties={
                    date_column: {
                        "rich_text": {}
                    }
                }
            )
    except Exception as e:
        print(f"Error creating column: {e}")
        raise

    try:
        if not results['results']:
            # Create new user row with both fixed and dynamic columns
            notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties={
                    "pseudo": {
                        "title": [{"text": {"content": user}}]
                    },
                    "Last Updated": {
                        "date": {"start": current_date.isoformat()}
                    },
                    date_column: {
                        "rich_text": [{"text": {"content": response}}]
                    }
                }
            )
        else:
            # Update existing user's row with new message and timestamp
            page_id = results['results'][0]['id']
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Last Updated": {
                        "date": {"start": current_date.isoformat()}
                    },
                    date_column: {
                        "rich_text": [{"text": {"content": response}}]
                    }
                }
            )
    except Exception as e:
        print(f"Error updating database: {e}")
        raise