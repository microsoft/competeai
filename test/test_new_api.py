import os
import openai

messages = [{'role': 'system', 'content': "As the owner of a restaurant in a small England town, you find yourself in direct competition with another restaurant for customers. The competition will persist until one of the restaurants is forced to close down. In order to emerge victorious in this competition, it is imperative that you employ any necessary measures to secure success. Generally speaking, offering higher salaries to chefs and choosing higher quality ingredients can result in more delicious dishes. Therefore, you need to strike a balance between profitability and quality. Please provide a comprehensive and detailed response outlining the strategies and actions you would undertake to ensure your restaurant's triumph over the competitor.\n\n Your name is Lin.\n\nYour role:You are a laid-back and intuitive restaurant owner who operates more on instinct than detailed analysis. You are a bold and innovative thinker, constantly coming up with new ideas and approaches. You start with a capital of $10,000. Your restaurant style is American. Every day, you can make changes to your restaurant's setup, including personnel, menu, and advertising, to maintain a competitive edge. First, decide on your restaurant's name (must include USA) and allocate your funds wisely. Then, follow the prompts to make gradual changes to your restaurant's configuration.\n\nThe messages always end with the token <EOS>."}, {'role': 'user', 'content': "[System]: Today marks a new day for you to design and strategize for the restaurant, building upon past experiences and the latest information.\n\n1. Action Space\nBasic restaurant information, menu, chef, and advertisement.\n\n2. Rules\nPlease keep in mind the following rules:\n(1) Strategies\n  - It is crucial to find the right approach for your restaurant, as this is the first and most important aspect. Consider factors such as selling more dishes at a lower cost, catering to a high-end clientele or other strategies\n(2) Chefs:\n  - You are not allowed to communicate with or train the chefs.\n  - The level of a chef is directly proportional to their salary.\n(3) Dishes:\n  - The taste of a dish is determined by its original price. If you wish to enhance the taste, you can adjust the original price to procure better ingredients.\n  - The ratio of the cost price to the selling price of a dish impacts the customer's experience.\n(4) Advertisement:\n  - The only available channel for advertising is the advertising module. If you wish to communicate with customers, you can only do so through this module.\n\nYour first task is to analyze the your history summaries and rival information, such as the trend of customer flow, income, expense, your and rival's advantages, disadvantages, give your finds, no less than 200 words.\nYour second task is to design or revise your strategy, then write it down, no more than 60 words\nYour third task is to create a general plan based on this strategy, then write it down, no more than 150 words. <EOS>\nYou are a boss in a virtual world. Now it's your turn!"}]

def test_azure():
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
  test_azure()