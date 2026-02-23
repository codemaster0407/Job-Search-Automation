import os
from huggingface_hub import InferenceClient
from huggingface_hub import login
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("HF_API_KEY")
login(api_key)

client = InferenceClient()



def call_llm(prompt):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return completion.choices[0].message