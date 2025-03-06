import json
import re

from dashboard.data_processing.LLM_formating.main import open_ai
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from dashboard.models import AiModel
from celery import shared_task
import base64


@shared_task
def process_ai_models_async(matched_pairs, ai_models_ids, model_config):
    print("Celery is running")
    ai_models = AiModel.objects.filter(id__in=ai_models_ids)


    for reg, part in matched_pairs:

        for model in ai_models:
            reg_content = reg['content']
            part_content = part['content']
            try:
                response = open_ai(reg_content, part_content, model, model_config)
                save_event_data(response)
                break
            except Exception as e:
                print(f"{model} Failed: {reg['name']} - {str(e)}")
                continue






def save_for_celery(file):
    file_content = base64.b64encode(file.read()).decode('utf-8')
    return {
        "name": file.name,
        "content": file_content,
        "content_type": file.content_type
    }




def save_event_data(response):
    pattern = r'```(?:json)?(.*?)```'
    match = re.search(pattern, response, re.DOTALL)

    if match:
        clean_string = match.group(1).strip()
    else:
        clean_string = response.strip()

    data = json.loads(clean_string)
    print(data)

