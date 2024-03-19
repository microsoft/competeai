# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import openai

def get_gpt_response(prompt):
    """ OpenAI 0.27 version"""
    # FIXME: v 0.28.1
    messages = [{'role': 'user', 'content': prompt}]
    completion = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )

    response = completion.choices[0]['message']['content']
    response = response.strip()
    print(response)
    return response

prompt = "Hello, Nice to meet you!"
get_gpt_response(prompt)