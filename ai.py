import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    raise EnvironmentError("Missing OPENAI_API_KEY in environment variables.")

openai_client = OpenAI(api_key=openai_key)

def get_response(prompt, model="gpt-4o", temperature=0.7):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error from OpenAI: {e}")
        return "⚠️ Unable to generate response."
