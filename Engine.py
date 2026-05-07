import os 
from dotenv import load_dotenv
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from notion_client import Client

   # --- 1. CONFIGURATION ---
load_dotenv() # This secretly loads your .env file into memory

   # Now Python pulls the token securely, without it being written here!
NOTION_TOKEN = os.getenv("NOTION_TOKEN") 
CHAR_DB_ID = "f64ee22b-e612-4531-942b-358a35559ecf" # DB IDs are safe to leave public
LOC_DB_ID = "ad92bcdd-aae5-4c47-93a1-838b6b1b0830"  

notion = Client(auth=NOTION_TOKEN)
   # ... (the rest of your code stays exactly the same)

# --- 2. THE SMARTER BRAIN SCHEMA ---
class Character(BaseModel):
    name: str = Field(description="Full name of the character")
    role: str = Field(description="Their role (e.g., Protagonist, Villain, Merchant)")
    description: str = Field(description="A short 1-sentence physical description")
    current_location: str = Field(description="The exact name of the location this character is currently in") # NEW!

class Location(BaseModel):
    name: str = Field(description="Name of the setting or place")
    vibe: str = Field(description="The atmosphere (e.g., Gritty, Magical, Industrial)")

class ScriptAnalysis(BaseModel):
    locations: List[Location]
    characters: List[Character] # AI will process locations first, then put characters in them

# --- 3. THE RELATIONAL ENGINE ---
def process_script_and_upload(text_chunk):
    print("🧠 1. Sending text to local AI...")
    
    client = instructor.from_openai(
        OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio"),
        mode=instructor.Mode.JSON_SCHEMA,
    )
    
    analysis = client.chat.completions.create(
        model="llama-3.1-8b",
        response_model=ScriptAnalysis,
        messages=[
            {"role": "system", "content": "You are a professional script editor extracting story data."},
            {"role": "user", "content": text_chunk},
        ],
    )
    print("✅ Extraction complete! Now uploading to Notion...")

    # Dictionary to remember the Notion IDs of the locations we create
    location_memory = {}

    # 1. Upload Locations FIRST
    for loc in analysis.locations:
        print(f"🗺️ Adding Location: {loc.name}")
        new_loc_page = notion.pages.create(
            parent={"database_id": LOC_DB_ID},
            properties={
                "Name": {"title": [{"text": {"content": loc.name}}]},
                "Vibe": {"rich_text": [{"text": {"content": loc.vibe}}]}
            }
        )
        # Save the Notion Page ID so we can link characters to it later!
        location_memory[loc.name.lower()] = new_loc_page["id"]

    # 2. Upload Characters and LINK them
    for char in analysis.characters:
        print(f"👤 Adding Character: {char.name}")
        
        properties_payload = {
            "Name": {"title": [{"text": {"content": char.name}}]},
            "Role": {"rich_text": [{"text": {"content": char.role}}]},
            "Description": {"rich_text": [{"text": {"content": char.description}}]}
        }

        # Check if the AI's current_location matches a location we just created
        ai_loc = char.current_location.lower()
        if ai_loc in location_memory:
            # THIS IS THE MAGIC: Linking the databases via API
            properties_payload["Location Link"] = {
                "relation": [{"id": location_memory[ai_loc]}]
            }
            print(f"   🔗 Linking {char.name} to {char.current_location}...")

        notion.pages.create(
            parent={"database_id": CHAR_DB_ID},
            properties=properties_payload
        )
    
    print("🎉 All Relational data pushed to your Notion Workspace!")

# --- 4. EXECUTION ---
if __name__ == "__main__":
    # This reads your script.txt file automatically
    with open("script.txt", "r", encoding="utf-8") as f:
        my_story_text = f.read()
    
    process_script_and_upload(my_story_text)