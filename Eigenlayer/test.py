from openai import OpenAI  # Ensure this is the latest SDK version
client = OpenAI(api_key="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")


chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Tell me some news about ETH in 2023"}
    ],
    model="gpt-4o",
)
print(chat_completion.choices[0].message.content)

