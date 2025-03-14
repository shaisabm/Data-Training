from openai import OpenAI



def open_router(registration, participants, model, default_model_config):
    client = OpenAI(
        api_key=default_model_config.api_key,
        base_url=default_model_config.base_url
    )

    registration_content = registration
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




