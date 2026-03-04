The service is an API (FastAPI + Uvicorn) that accepts form data.

Input parameters (one of the two is required):
• db_documents_id: int — document ID in the database
• file: file — image file for processing

File requirements
• Supported image formats: JPEG, PNG, BMP, and others supported by the PIL library
• Recommended resolution: at least 300 DPI for optimal QR code recognition

Error handling
• 400 Bad Request — client‑side error: required parameters missing or file reading error; the response describes the error
• 500 Internal Server Error — server‑side error: failure to retrieve data from the database

Build instructions

python3.8 -m venv venv38

source venv38/bin/activate

pip install -r requirements.txt

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

------------------------------------------------------------------------------------------------------------------------------
Сервис представляет собой API(fastapi+uvicorn) 

Принимает formdata 

На вход принимается один из двух параметров:

•	db_documents_id: int - ID документа в базе данных 

•	file: File* - Файл изображения для обработки

*Требования к файлам

•	Поддерживаются форматы изображений: JPEG, PNG, BMP и другие, поддерживаемые библиотекой PIL

•	Рекомендуемое разрешение: не менее 300 DPI для лучшего распознавания QR-кодов


Обработка ошибок:

•	400 Bad Request - клиентская: не указаны обязательные параметры или ошибка чтения файла, в респонсе описывается ошибка

•	500 Internal Server Error - серверная: ошибка получения данных из БД


Инструкция по сборке: 

python3.8 -m venv venv38

source venv38/bin/activate

pip install -r requirements.txt

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
