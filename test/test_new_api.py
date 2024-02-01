import os
import openai

content = """
You are outstanding behavior analysts. Now you need to analyze the reason of customer choices. Next is the thought process of customer:
 "Classic American Diner offers a higher customer score and dishes that suit my dairy-free requirement. The Savory Vegan Delight and Smoked Caesar Salad cater to my sophisticated palate."

This customer role description is 
$14500 (Affluent),Gourmet dishes,Lactose intolerant,Dairy-free,Sophisticated

Please choose single or multi options:

A: Meet core needs ( Align with diet restriction or taste)
B: Brand Loyalty ( customer previous experience)
C: Public Praise ( High Score or Positive comments)
D: More Affordable or Reasonable
E: Innovation  or Improvement

Only output all answer (A-E)
"""

messages_example = [{'role': 'assistant', 'content': content}]

def test_azure():
  print("test_azure")
  openai.api_type = "azure"
  openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
  openai.api_version = "2023-07-01-preview"
  openai.api_key = os.getenv("AZURE_OPENAI_KEY")
  
  message_text = messages
  
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
  openai.api_key = "sk-xxx"
  
  # modelList =openai.Model.list()
  # print(modelList)
  
  messages = messages_example
  
  completion = openai.ChatCompletion.create(
          model='gpt-4-1106-preview',
          messages=messages_example,
          temperature=0.7,
          max_tokens=800,
      )
  response = completion.choices[0].message.content
  response = response.strip()
  print(response)
  
  
if __name__ == "__main__":
  test_openai()