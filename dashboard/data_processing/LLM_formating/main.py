from openai import OpenAI
import pandas as pd
import os
import time


def open_ai(registration, participants, model, default_model_config):
    client = OpenAI(
        api_key=default_model_config.api_key,
        base_url=default_model_config.base_url
    )

    registration_content = registration
    print(registration_content)

    participants_content = participants

    completion = client.chat.completions.create(

        model=model.ai_model,
        messages=[
            {
                "role": "system",
                "content": default_model_config.system_instructions
            },
            {
                "role": "user",
                "content": f"Registration Content:\n{registration_content}\n\nParticipants Content:\n{participants_content}"
            }
        ]
    )

    return  completion.choices[0].message.content



