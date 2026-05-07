from notion_client import Client

NOTION_TOKEN = "ntn_A56648997424eU5Xs2JDX1dYWFXn5jJz4p3zUYl0WJN8Fk" # Paste your Notion token here
CHAR_DB_ID = "f64ee22b-e612-4531-942b-358a35559ecf"

notion = Client(auth=NOTION_TOKEN)

def check_columns():
    db = notion.databases.retrieve(database_id=CHAR_DB_ID)
    print("📋 Current Columns in your Notion Database:")
    for prop_name in db["properties"].keys():
        print(f"- {prop_name}")

if __name__ == "__main__":
    check_columns()