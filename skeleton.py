from notion_client import Client

# 1. SETUP: Your Notion Credentials
NOTION_TOKEN = "ntn_A56648997424eU5Xs2JDX1dYWFXn5jJz4p3zUYl0WJN8Fk" # Paste your internal integration token
PARENT_PAGE_ID = "358151a7829e80f9a316e4035be29ec4"      # Paste the 32-character page ID

# Initialize the Notion Client
notion = Client(auth=NOTION_TOKEN)

def build_workspace():
    print("🏗️ Building the Peace Break Workspace in Notion...")

    # 2. Create the Characters Database
    char_db = notion.databases.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        title=[{"type": "text", "text": {"content": "Master Character Cast"}}],
        properties={
            "Name": {"title": {}}, # Every Notion DB needs exactly one 'title' property
            "Role": {"rich_text": {}},
            "Description": {"rich_text": {}}
        }
    )
    print(f"✅ Characters Database created! (ID: {char_db['id']})")

    # 3. Create the Locations Database
    loc_db = notion.databases.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        title=[{"type": "text", "text": {"content": "World Locations"}}],
        properties={
            "Name": {"title": {}},
            "Vibe": {"rich_text": {}}
        }
    )
    print(f"✅ Locations Database created! (ID: {loc_db['id']})")
    
    return char_db['id'], loc_db['id']

# Execute the function
if __name__ == "__main__":
    build_workspace()