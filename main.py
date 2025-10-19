import os
import io
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from zeep import Client
from PIL import Image
from proccessing import load_models, predict_and_compare, decode_qr_code
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# инициализация моделей один раз при старте
models = load_models()

WSDL_URL = os.getenv("url")
api_key = os.getenv("api_key")
client = Client(WSDL_URL)

@app.post("/predict")
async def predict_document(
    db_documents_id: int = Form(None),
    file: UploadFile = None
):
    try:
        # Получение файла
        if db_documents_id:
            try:
                file_bytes = client.service.Method(
                    db_documents_id,
                    api_key
                )
                image = Image.open(io.BytesIO(file_bytes))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ошибка получения из DocumentService: {e}")
        elif file:
            try:
                contents = await file.read()
                image = Image.open(io.BytesIO(contents))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Ошибка открытия файла: {e}")
        else:
            raise HTTPException(status_code=400, detail="Нужно прислать либо db_documents_id, либо файл")

        # пайплайн
        result = predict_and_compare(image=image, models=models)

        if result['confidence'] < 0.5:
            result['best_model'] = ['ни один из']
            dict_patent = {}
        elif result['best_model'] == 'обратный патент':
            dict_patent = decode_qr_code(image)
        else:
            dict_patent = {}

        return JSONResponse(
            content={
                "тип документа": result['best_model'],
                "инфа по патенту": dict_patent,
                "уверенность": result.get("confidence", None)
            }
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {e}")
