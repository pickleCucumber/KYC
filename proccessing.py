from ultralytics import YOLO
import numpy as np
from zeep import Client
import os
import io
from PIL import Image
from qreader import QReader

def load_models():
    models_paths = [
    r'final_cls\vnz_cls\weights\best.pt',
    r'final_cls\patent_cls\weights\best.pt',
    r'final_cls\return_patent_cls\weights\best.pt',
    r'final_cls\rvp_cls\weights\best.pt'
        ]
    names = ['ВНЖ', 'патент', 'обратный патент', 'РВП']
    models = []
    for i, (model_path, name) in enumerate(zip(models_paths, names)):
        print(f"Загрузка модели {i+1}: {model_path}")
        model = YOLO(model_path)
        models.append({
            'model': model,
            'name': name,
            'path': model_path,
        })
    return models

def predict_and_compare(image, models, target_class_index=1):
    results = {}

    for model_info in models:
        model = model_info['model']
        model_name = model_info['name']

        prediction = model.predict(image)
        result = prediction[0]  # берем первый результат

        # получаем вероятности для всех классов
        all_probs = result.probs.data.tolist()
        top1_index = result.probs.top1
        top1_confidence = result.probs.top1conf.item()
        class_name = result.names[top1_index]

        # результаты
        results[model_name] = {
            'all_probs': all_probs,
            'top1_index': top1_index,
            'top1_confidence': top1_confidence,
            'top1_class_name': class_name,
            'class_names': result.names
        }

    # Анализ результатов
    if target_class_index is not None:
        # сравнение уверенности в конкретном классе
        target_confidences = {}

        for model_name, model_data in results.items():
            target_confidences[model_name] = model_data['all_probs'][target_class_index]

        # выбор модели с наибольшей уверенностью в целевом классе
        best_model_name = max(target_confidences.items(), key=lambda x: x[1])[0]
        final_class_index = target_class_index
        final_confidence = target_confidences[best_model_name]
        final_class_name = results[best_model_name]['class_names'][target_class_index]

    # итог словарь
    final_result = {
        'selected_class_index': final_class_index,
        'selected_class_name': final_class_name,
        'confidence': final_confidence,
        'best_model': best_model_name,
        'all_results': results
    }

    return final_result


def decode_qr_code(image):
    qr_reader = QReader()

    try:
       # image = Image.open(image_path).convert('RGB')
        np_image = np.array(image)

        result = qr_reader.detect_and_decode(np_image)

        # Формируем словарь с результатом
        if result and result[0]:
            qr_data = result[0]
            return {
                'status': 'success',
                'qr_code_data': qr_data,
                'message': 'QR-код успешно распознан'
            }
        else:
            return {
                'status': 'error',
                'qr_code_data': None,
                'message': 'QR-код не найден или не распознан'
            }

    except Exception as e:
        return {
            'status': 'error',
            'qr_code_data': None,
            'message': f'Ошибка при обработке изображения: {str(e)}'
        }