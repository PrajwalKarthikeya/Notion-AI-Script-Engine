import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# 1. SETUP: This connects Python to your LM Studio server
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:1234/v1", # This is the address LM Studio gave you
        api_key="lm-studio",                 # LM Studio doesn't need a real key
    ),
    mode=instructor.Mode.JSON_SCHEMA,
)

# 2. THE SCHEMA: Think of this as the "Form" the AI must fill out
class Character(BaseModel):
    name: str = Field(description="Full name of the character")
    role: str = Field(description="Their role (e.g., Protagonist, Villain, Merchant)")
    description: str = Field(description="A short 1-sentence physical description")

class Location(BaseModel):
    name: str = Field(description="Name of the setting or place")
    vibe: str = Field(description="The atmosphere (e.g., Gritty, Magical, Industrial)")

class ScriptAnalysis(BaseModel):
    characters: List[Character]
    locations: List[Location]
    summary: str = Field(description="A 2-sentence summary of what happens in this scene")

# 3. THE EXECUTION: We give the AI a snippet of Peace Break to analyze
sample_text = """
The relief of the Weeping Valley command is not a ceremony; it is an eviction. Major Eland Vorstrum arrives in a pristine
transport, stepping into the blood-soaked mud with a handkerchief pressed to his nose. He surveys the battered Squad and the
unconscious Solhallow with undisguised contempt. "You’ve made quite a mess," Vorstrum sneers, adjusting his clean uniform.
"Go back to the capital and wave at the cameras. Real officers will hold the line now." He effectively steals the command, eager to
take credit for the defense now that the hard fighting is done. As the Squad loads onto the transport, Vorstrum glares at Kaito.
"Don't think a few dead assassins make you a hero, Veyrune. You're still just a Dominion battery waiting to leak."
The journey to the Astra Capital is a surreal nightmare. The Squad is moved from the transport truck into a sleek, black
government limousine provided by the Zhàn delegation. They enter the city not as soldiers, but as props. The streets are lined
with thousands of civilians waving Astra flags, cheering for "The Heroes of the Valley." Confetti rains down on the car. Inside, the
silence is deafening. Arrow stares at his healed but scarred hands; Seris looks out the window, ignoring the banners bearing her
family crest. Kaito feels bile rising in his throat. To the crowd, this is a victory. To the Squad, it feels like a funeral procession for
the friends they left in the mud.
Upon arrival, the Squad immediately go to the "Imperial Wing" of the central hospital—a sector entirely requisitioned by the Zhàn
delegation. Ren and Solhallow are being treated there. When Kaito and Saira try to follow, they are blocked by two towering Zhàn
guards. "Restricted access," one states flatly. "Prince Lin’s guests only." Kaito argues, panic setting in, but Senator Lysandra
Veyrune appears from the hallway. She places a hand on Kaito’s shoulder—cold, calculating, familial. "Don't fight the hand that
feeds us, Kaito," she whispers. "Your brother is being treated by the finest doctors in the world. Let the Zhàn have their pets. You
have a role to play elsewhere."
In the Grand War Room, the tension is suffocating. Emperor Han Xuan stands up in the middle of Prime Minister Caelum’s
speech about logistics. "I am bored," Han announces, his voice silencing the room. "This war is moving too slowly. I have an
empire to run." He gestures to his eldest son, Crown Prince Jian Xuan. "Jian will speak for Zhàn. Do not waste his time." Han
leaves without looking back, treating the Astra government like a dull dinner party. Jian sits, and the atmosphere shifts from regal
to terrifyingly efficient. "We are done defending," Jian states, ignoring the Astra generals. "We are drafting a counter-offensive.
Astra will provide the bodies; Zhàn will provide the direction."
Meanwhile, in the restricted Imperial Wing, the atmosphere is disturbingly domestic. Ren wakes up not in a hospital bed, but in a
luxurious suite filled with silk and incense. Solhallow is in the next bed, still comatose, hooked up to machines that look more like
art than medical tech. Princess Mei is arranging flowers in a vase, while Lin Xuan sits by Ren’s bedside, peeling an orange.
"Welcome back to the land of the living, Little Radar," Lin smiles, offering a slice. "Your brother was very loud. It was... inspiring."
Ren pulls back, terrified. "Where is Kaito?" Lin chuckles, patting Ren’s hand. "Safe. For now. But he is a very volatile element,
isn't he? Perhaps he needs a better handler."
Back at the barracks, the Squad is given VIP quarters, but they feel like prison cells. Saira Munthir (Bharatyr) wanders the halls,
disgusted by the opulence of the Astra capital while the border burns. She meets Instructor Draave Thornwell, who is drunk and
bitter, leaning against a pillar. "Heroes," Draave spits, looking at the Squad. "They’ll put you on a poster today and in a grave
tomorrow. Enjoy the champagne, kids." The cynicism of the Old Guard weighs heavily on them. They realize they aren't safe here;
they are just assets being polished for the next slaughter.
Kaito enters his solitary room, exhausted and isolated. He finds a sleek, black box sitting on his bed. There is no sender address,
only the golden seal of the Xuan Dynasty. He opens it. Inside, folded neatly, is a high-collared military uniform. It isn't the blue of
Astra. It is the deep, midnight black and gold of the Zhàn elite guard, tailored perfectly to his measurements.
A note sits on top, written in elegant calligraphy:"Blue is the color of bruises. Gold is the color of kings. Dinner is at 8. — Lin."
Kaito stares at the uniform. It represents safety, power, and betrayal. He touches the fabric, and for the first time, he wonders if
fighting for Astra—a country that fears him and sells its soldiers—is truly the only choice. The episode ends with Kaito standing in
front of the mirror, holding the black jacket against his chest, as the reflection seems to darken around him.
"""

print("🧠 The Brain is thinking... please wait.")

# This sends the text to your local Llama-3 model
response = client.chat.completions.create(
    model="llama-3.1-8b", # This name doesn't matter much for LM Studio
    response_model=ScriptAnalysis,
    messages=[
        {"role": "system", "content": "You are a professional script editor extracting story data."},
        {"role": "user", "content": sample_text},
    ],
)

# 4. THE OUTPUT: Let's see what it found!
print("\n--- EXTRACTION COMPLETE ---")
print(f"SUMMARY: {response.summary}")
print("\nCHARACTERS FOUND:")
for char in response.characters:
    print(f"- {char.name} ({char.role}): {char.description}")

print("\nLOCATIONS FOUND:")
for loc in response.locations:
    print(f"- {loc.name} (Vibe: {loc.vibe})")