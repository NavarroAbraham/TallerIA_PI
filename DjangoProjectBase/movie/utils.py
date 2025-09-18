

import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

def get_completion(prompt, model="gpt-3.5-turbo"):
    load_dotenv('openAI.env')
    client = OpenAI(api_key=os.environ.get('openai_apikey'))
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def get_embedding(text):
    load_dotenv('openAI.env')
    client = OpenAI(api_key=os.environ.get('openai_apikey'))
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return np.array(response.data[0].embedding, dtype=np.float32)