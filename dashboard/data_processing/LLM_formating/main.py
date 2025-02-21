from openai import OpenAI
import pandas as pd


def open_ai(registration, participants, model_config):
    # client = OpenAI(
    #     api_key=model_config.api_key,
    #     base_url=model_config.base_url
    # )
    #
    # df_registration = pd.read_csv(registration)
    # registration_content = df_registration.to_string()
    #
    # df_participants = pd.read_csv(participants)
    # participants_content = df_participants.to_string()
    #
    # completion = client.chat.completions.create(
    #
    #     model=model_config.ai_model,
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": model_config.system_instructions
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Registration Content:\n{registration_content}\n\nParticipants Content:\n{participants_content}"
    #         }
    #     ]
    # )
    #
    # print(completion.choices[0].message.content)
    pass

