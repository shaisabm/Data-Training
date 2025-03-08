import json
import re

from dashboard.data_processing.LLM_formating.main import open_ai
from dashboard.models import AiModel, DefaultAiConfig, MasterDB
from celery import shared_task
import base64
from jsonschema import validate
from dashboard.models import ExcludedIndividual
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@shared_task
def process_ai_models_async(matched_pairs):
    print(f"Celery is running! \n"
          f"{len(matched_pairs)} pairs of files to process")

    pair_to_process = len(matched_pairs)
    ai_models = AiModel.objects.all()
    default_model_config = AiModel.get_defaults()

    for i, (reg, part) in enumerate(matched_pairs):

        for model in ai_models:
            reg_content = reg['content']
            part_content = part['content']
            try:
                response = open_ai(reg_content, part_content, model, default_model_config)
                if response is None:
                    print(f"No response from {model}. Trying next the model if available.")
                    continue
                print(f"Received response from {model}")
                save_event_data(response, default_model_config, i, pair_to_process)
                break
            except Exception as e:
                print(f"{model} Failed: {reg['name']} - {str(e)}")
                continue


def save_for_celery(file):
    default_storage.save(f'temp/{file.name}', ContentFile(file.read()))

    file_content = base64.b64encode(file.read()).decode('utf-8')
    return {
        "name": file.name,
        "content": file_content,
        "content_type": file.content_type
    }


def save_event_data(response, default_model_config, i, pair_to_process):
    pattern = r'```(?:json)?(.*?)```'
    match = re.search(pattern, response, re.DOTALL)

    if match:
        clean_string = match.group(1).strip()
    else:
        clean_string = response.strip()

    data = json.loads(clean_string)
    print("Data successfully converted to json")

    schema = default_model_config.json_validation_schema
    validate(instance=data, schema=schema)
    print("Data passed schema validation")

    event_data = data['event']
    participants_data = data['participants']
    zoom_id = event_data['id']

    excluded_emails = ExcludedIndividual.get_all_emails()


    for participant in participants_data:
        first_name = participant['first_name']
        last_name = participant['last_name']
        email = participant['email'].lower().strip()

        if email in excluded_emails: continue

        exists_by_name = MasterDB.objects.filter(first_name=first_name, last_name=last_name, zoom_id=zoom_id).exists()
        exists_by_email = MasterDB.objects.filter(email=email, zoom_id=zoom_id).exists()


        if not (exists_by_name or exists_by_email):
            MasterDB.objects.update_or_create(
                topic= event_data['topic'],
                zoom_id = zoom_id,
                event_month = event_data['event_month'],
                event_date = event_data['event_date'],
                event_time = event_data['event_date'],
                first_name = participant['first_name'],
                last_name = participant['last_name'],
                email = email,
                join_time = participant['join_time'],
                leave_time = participant['leave_time'],
                duration = participant['duration'],
                attended = participant['attended']

            )
    print(f"Data has been added to the DB ({i+1}/{pair_to_process})")
