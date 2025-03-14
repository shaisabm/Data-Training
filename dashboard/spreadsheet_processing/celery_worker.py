import json
import os.path
import re
from sqlite3 import IntegrityError

from dashboard.data_processing.LLM_formating.main import open_router
from dashboard.models import AiModel, DefaultAiConfig, MasterDB
from celery import shared_task
import base64
from jsonschema import validate
from dashboard.models import ExcludedIndividual
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@shared_task
def process_ai_models_async(matched_pairs):
    print(f"Processing the data! "
          f"{len(matched_pairs)} pairs of spreadsheet to process...")

    pairs_to_process = len(matched_pairs)
    ai_models = AiModel.objects.all()
    default_model_config = AiModel.get_defaults()

    for i, (reg, part, name) in enumerate(matched_pairs):

        for m in range(len(ai_models)):
            try:
                response = open_router(reg, part, ai_models[m], default_model_config)
                if response is None:
                    print(f"[{name}] {m+1}/{len(ai_models)} No response from {ai_models[m]}")
                    continue
                print(f"[{name}] Received response from {ai_models[m]}")
                save_event_data(response, default_model_config, i, pairs_to_process, name)
                break
            except Exception as e:
                print(f"[{name}] {m+1}/{len(ai_models)} {ai_models[m]} error occurred: {str(e)}")
                continue



def save_event_data(response, default_model_config, i, pairs_to_process, name):
    pattern = r'```(?:json)?(.*?)```'
    match = re.search(pattern, response, re.DOTALL)

    if match:
        clean_string = match.group(1).strip()
    else:
        clean_string = response.strip()

    data = json.loads(clean_string)
    print(f"[{name}] Data successfully converted to json")

    schema = default_model_config.json_validation_schema
    validate(instance=data, schema=schema)
    print(f"[{name}] Data passed schema validation")

    event_data = data['event']
    participants_data = data['participants']
    zoom_id = int(event_data['id'])

    excluded_emails = ExcludedIndividual.get_all_emails()


    for participant in participants_data:
        first_name = participant['first_name'].capitalize()
        last_name = participant['last_name'].capitalize()
        email = participant['email'].lower().strip()

        if email in excluded_emails: continue

        exists_by_name = MasterDB.objects.filter(first_name=first_name, last_name=last_name, zoom_id=zoom_id).exists()
        exists_by_email = MasterDB.objects.filter(email=email, zoom_id=zoom_id).exists()

        if not (exists_by_name or exists_by_email):
            try:
                MasterDB.objects.update_or_create(
                    topic= event_data['topic'],
                    zoom_id = zoom_id,
                    event_month = event_data['event_month'],
                    event_date = event_data['event_date'],
                    event_time = event_data['event_date'],
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    join_time = participant['join_time'],
                    leave_time = participant['leave_time'],
                    duration = participant['duration'],
                    attended = participant['attended']

                )
            except IntegrityError:
                print(f"[{name}] Duplicate entry detected. Skipping...")

    print(f"[{name}] ({i+1}/{pairs_to_process}) has been added to the DB")

def save_for_celery(file):

    file_content = file.read()
    return file_content.decode('utf-8')
