import os
import openai


def test_azure():
  openai.api_type = "azure"
  openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
  openai.api_version = "2023-07-01-preview"
  openai.api_key = os.getenv("AZURE_OPENAI_KEY")
  
  message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
  
  completion = openai.ChatCompletion.create(
    engine="gpt-4-1106",
    messages = message_text,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
  )

  response = completion.choices[0].message.content
  response = response.strip()
  print(response)

def test_openai():
  openai.api_key = os.getenv("OPENAI_KEY")
  
  messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
  
  completion = openai.ChatCompletion.create(
          model='gpt-4-vision-preview',
          messages=messages,
          temperature=0.7,
          max_tokens=800,
      )
  response = completion.choices[0].message.content
  response = response.strip()
  print(response)
  
  
if __name__ == "__main__":
  while True:
    test_openai()