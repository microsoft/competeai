# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import base64
import os

# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# image_path = "competeai/logs/test_pic/menu.png"

# base64_image = encode_image(image_path)

# message0 = {"role": "user", "content": "Two picture differences?"}

# message1 = {
#     "role": "user",
#     "content": [
#         {"type": "text", "text": "The first picture we are talking about"},
#         {
#             "type": "image_url",
#             "image_url": {
#             "url": f"data:image/jpeg;base64,{base64_image}",
#             },
#         },
#     ],
# }

message2 = {
    "role": "user",
    "content": [
        {"type": "text", "text": "The second picture we are talking about"},
        {
            "type": "image_url",
            "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
        },
    ],
}

openai_api_key = os.environ.get("OPENAI_KEY")

""" openai 1.00 version"""

# from openai import OpenAI

# client = OpenAI(api_key=openai_api_key)
# response = client.chat.completions.create(
#   model="gpt-4-vision-preview",
#   messages=[
#     message0,
#     message1,
#     message2,
#   ],
#   max_tokens=300,
# )

# print(response.choices[0].message.content)

""" openai 0.27 version """

import openai

openai.api_key = openai_api_key
completion = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            # message0,
            # message1,
            message2,
        ],
        max_tokens=300,
)

response = completion.choices[0]['message']['content']
response = response.strip()

print(response)