import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv('PERPLEXITY_API_KEY')
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

prompt = "What are the top 5 most popular TikTok videos right now about personal growth? List their direct video URLs."

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)
