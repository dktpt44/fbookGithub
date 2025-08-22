import openai
import os
import sys

if len(sys.argv) == 3:
    question = sys.argv[1]
    language = sys.argv[2]
    prompt = question + ', please answer in ' + language
else:
    print("Usage: python your_script.py <question> <language>")
    sys.exit(1)

api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

# Use the new client interface
client = openai.OpenAI()

#def chat(prompt, model="gpt-3.5-turbo", max_tokens=300):
#def chat(prompt, model="gpt-4o-mini", max_tokens=1000):
def chat(prompt, model="gpt-4.1-mini", max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

try:
    print(chat(prompt))
except Exception as e:
    print("Error from OpenAI:", e)
