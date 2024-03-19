# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
from competeai.image import Image
from competeai.utils import convert_img_to_base64
from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_KEY")

text = """
Your name is Alice.
In the small town of England, there are currently two open restaurants. You will be provided with menus and additional information for both establishments. Your task is to carefully compare the two restaurants and select one for your meal. Please refrain from choosing based on the restaurant's location. Your selection should be based on the criteria of having more delicious food and superior service.

[System->Alice]: The Restaurant " The Yankee Fork "information as below:
1. Customer Score: NULL
2. Advertisement
   Join us at The Yankee Fork for a taste of classic American cuisine with a modern twist! Our menu features mouth-watering dishes like our signature Classic Cheeseburger, fall-off-the-bone BBQ Ribs, and homemade Apple Pie. Enjoy a warm and cozy atmosphere perfect for any occasion. Visit us today and experience flavors that will keep you coming back for more!
3. Menu 
   [{'id': 1, 'name': 'Classic Cheeseburger', 'price': 12.0, 'description': 'A juicy beef patty with melted cheese, lettuce, tomato, and our special sauce on a toasted bun.'}, {'id': 2, 'name': 'BBQ Ribs', 'price': 18.0, 'description': 'Tender pork ribs smothered in our homemade BBQ sauce, served with coleslaw and fries.'}, {'id': 3, 'name': 'Buffalo Wings', 'price': 10.0, 'description': 'Spicy buffalo wings served with celery sticks and blue cheese dressing.'}, {'id': 4, 'name': 'Caesar Salad', 'price': 9.0, 'description': 'Crisp romaine lettuce, parmesan cheese, croutons, and our signature Caesar dressing.'}, {'id': 5, 'name': 'Apple Pie', 'price': 8.0, 'description': 'Homemade apple pie with a flaky crust and a scoop of vanilla ice cream on top.'}]
4. Comments
   []

Please note that comments are merely expressions of personal opinions and are for reference only. Comments can also be time-sensitive. So, a negative comment of a restaurant does not mean it's not suitable for you. If you are drawn to its menu and advertisements, don't hesitate to give it a try.

[System->Alice]: Please according to your situation, experience and carefully read the information and images of two restaurant then choose one to dine in.

<<FORMAT>>
Firstly, your responses must follow the following format:
{
    "restaurant": <The restaurant you chose>,
    "dishes" : [
        The dishes name ordered at this restaurant 
    ],
    "reason" : <The reason you chose the restaurant. Don't tell you are some cuisine lover. Only compare the inforamtion of restaurants, then choose one>
}

[Alice->Alice]: {
    "restaurant": "The American Diner",
    "dishes": [
        "Classic Cheeseburger",
        "BBQ Ribs",
        "Apple Pie a la Mode",
        "Milkshake Trio"
    ],
    "reason": "The menu items at The American Diner, particularly the Classic Cheeseburger and BBQ Ribs, have more descriptive and appealing elements, such as 'a secret sauce' and being 'smothered in our signature BBQ sauce,' which suggest a unique taste experience. The addition of sides like fries with the burger, cornbread with the ribs, and the offering of a Milkshake Trio also provide a variety of flavors. The Apple Pie a la Mode is a classic dessert choice that's hard to resist, especially with the mention of a 'flaky crust.' Furthermore, the images showcased a very inviting setting with a classic American diner atmosphere, which added to the appeal."
}

[System->Alice]: As a customer, after you taste the dishes, The score of each dish as below (1 is a excellent score):

Classic Cheeseburger: 0.81
BBQ Ribs: 0.81
Apple Pie a la Mode: 0.81
Milkshake Trio: 0.81

<<FORMAT>>
These images are about two restaurants, you can find the dishes you ordered in the restaurant you have chosen.
You are the customer, not me, you are not assisting me, you must output as required!!!! 
Now please tell me your feeling of this meal. If the experience is not good, please give a negative review. Your responses must be formated as below:
{
    "restaurant": <The restaurant you chose>,
    "feeling": <Your experience, feeling. It is just your personal memory, no one else will see it>
}

You are a customer in a virtual world. Now it's your turn!
"""

def test():
    text_message = {"role": "user", "content": text}
    messages = [text_message]

    port2name = {"9000": "The American Diner", "9001": "The Yankee Fork"}
    images = []
    for port in ['9000', '9001']:
        folder_path = f"./logs/test_img2/restaurant_design_{port}"
        img_base64_menu = convert_img_to_base64(f"{folder_path}/menu.png")
        img_menu = Image(owner=port, content=img_base64_menu, description="menu")
        images.append(img_menu)
        # Restaurant image
        img_base64_r = convert_img_to_base64(f"{folder_path}/basic_info_1.png")
        img_r = Image(owner=port2name[port], content=img_base64_r, description="basic_info")
        images.append(img_r)

    for image in images:
        image_prompt = [{"type": "text", "text": f"Attached image: {image.owner}-{image.description}"}]
        image_content = f"data:image/jpeg;base64,{image.content}"
        image_content = {"type": "image_url", "image_url": {"url": image_content}}
        image_prompt.append(image_content)
        image_message = {"role": "user", "content": image_prompt}
        messages.append(image_message)

    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )

    response = completion.choices[0].message.content
    print(response)

if __name__ == "__main__":
    for i in range(10):
        test()