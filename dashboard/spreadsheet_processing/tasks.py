from dashboard.data_processing.LLM_formating.main import open_ai
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from dashboard.models import AiModel
from celery import shared_task



@shared_task
def process_ai_models_async(matched_pairs, ai_models_ids, model_config):
    print("process ai models running")
    ai_models = AiModel.objects.filter(id__in=ai_models_ids)

    for reg, part in matched_pairs:

        with default_storage.open(reg) as reg_file, default_storage.open(part) as part_file:
            for model in ai_models:
                try:
                    result = open_ai(reg_file, part_file, model, model_config)
                    print(result)
                    break
                except Exception as e:
                    print(f"Failed: {reg.name} - {str(e)}")
                    continue
                finally:
                    if reg:
                        default_storage.delete(reg)
                    if part:
                        default_storage.delete(part)





def save_uploaded_file(file):
    if file:
        file_path = f'temp/{file.name}'
        path = default_storage.save(file_path, ContentFile(file.read()))
        return path
