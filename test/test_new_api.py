from openai import AzureOpenAI
import os

# client = OpenAI(
#     api_type="azure",
#     api_base="https://janiceaoai-caeast.openai.azure.com/",
#     api_version="2023-07-01-preview",
#     api_key="bba0bf94ca544cf4a3ba5e8321558641"
# )

# completion = client.chat.completions.create(
#     model= "gpt-4-turbo",
#     messages={"role": "system", "content": "Your name is Janice.\n\nYour role:You are a customer in a virtual world. Now it's your turn!"},
#     temperature=0.7,
#     max_tokens=300
# )

# response = completion.choices[0].message.content
# response = response.strip()

# print(response)
 
# openai.api_type = "azure"
# openai.api_base = "https://janiceaoai-caeast.openai.azure.com/"
# openai.api_version = "2023-07-01-preview"
# openai.api_key = "bba0bf94ca544cf4a3ba5e8321558641"
 
# print(os.getenv("AZURE_OPENAI_ENDPOINT"))
# print(os.getenv("AZURE_OPENAI_KEY"))
 
# messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
 
# client = AzureOpenAI(
#   azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
#   api_key=os.getenv("AZURE_OPENAI_KEY"),  
#   api_version="2023-05-15"
# )
     
# completion = client.chat.completions.create(
#     model="gpt-35-turbo",
#     messages=messages,
#     temperature=0.7,
#     max_tokens=300
# )

# response = completion.choices[0].message.content
# response = response.strip()
# print(response)

import os
import openai
 
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
 
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