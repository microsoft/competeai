# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

response = openai.Image.create(
    model="dall-e-3",
    prompt="a big apple",
    size='1024x1024',
    quality="standard",
    response_format="url",
    n=1,
) 

print(response)