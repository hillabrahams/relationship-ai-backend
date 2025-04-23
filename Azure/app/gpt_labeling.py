import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Try GPT-4-turbo, fall back to GPT-3.5-turbo if needed
def get_gpt_label(text: str, model: str = "gpt-4-turbo") -> dict:
    system_prompt = """
You are an expert relationship therapist AI. Your task is to evaluate journal entries and assign a sentiment score from -10 (abuse) to +10 (care), with 0 representing neglect.

Return a JSON with:
- score: a number between -10 and 10
- reasoning: a 1-2 sentence explanation
- confidence: a number from 0 to 1
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f'Entry: "{text}"'}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.4
        )
    except openai.error.InvalidRequestError as e:
        if "does not exist" in str(e) and model == "gpt-4-turbo":
            print("⚠️ GPT-4-turbo not available — falling back to GPT-3.5-turbo")
            return get_gpt_label(text, model="gpt-3.5-turbo")
        else:
            raise e

    content = response['choices'][0]['message']['content']
    print("GPT Response:", content)

    try:
        return json.loads(content)
    except Exception:
        return {
            "score": 0,
            "reasoning": "Could not parse GPT response",
            "confidence": 0
        }
