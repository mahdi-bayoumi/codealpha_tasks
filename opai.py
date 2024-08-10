import os
import openai
from openai import OpenAI, OpenAIError

# Set your API key
api_key = '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'
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")
else:
    print("API key found")
openai.api_key = api_key

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)
try:
    # Use a model available in the free tier
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # Update if necessary based on available models
        messages=[{"role": "system", "content": "hello"}],
        max_tokens=150,
        response_format={"type": "json_object"}  # Use "response_format" for clarity
    )
    print(response.choices[0].text.strip())

    # Use gpt-3.5-turbo for chat completion
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say this is a test"},
        ]
    )
    print(chat_response.choices[0].message['content'].strip())

except OpenAIError as e:
    print(f"An error occurred: {e}")
