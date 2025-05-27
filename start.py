from openai import OpenAI

# Key by EmreSevinc don't use recklessly.
client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);

