import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

TRIGGER_PHRASES = [
    "suicide",
    "kill myself",
    "self harm",
    "want to die"
]

DISCLAIMER = "If you're feeling unsafe or overwhelmed, please consider reaching out to someone you trust or a local support service."

def check_triggers(note):
    note_lower = note.lower()
    for phrase in TRIGGER_PHRASES:
        if phrase in note_lower:
            return True
    return False

def get_vibe_check(note):
    if not note or len(note) < 50:
        return None

    if check_triggers(note):
        return DISCLAIMER

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive, non-clinical mental health assistant. Respond to the user's journal entry in 1-2 sentences. Maintain a calm tone. Avoid diagnosis. Avoid crisis instructions."},
                {"role": "user", "content": note}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "I'm having trouble connecting to my thoughts right now, but I'm listening."
