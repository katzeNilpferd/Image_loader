# Image Uploader (Test)

Праллельная загрузка картинок на сервер
с ограничением количества одновременных загрузок.

## Установка

Требуется Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `UPLOAD_URL` | `http://127.0.0.1:8000/upload` | URL эндпоинта загрузки |
| `MAX_WORKERS` | `4` | Максимальное количество потоков загрузки |
| `IMAGES_DIR` | `./images` | Папка с изображениями |

## Запуск

1. Запуск тестового сервера:

   ```bash
   cd .test/server
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. Генерация тестовых изображений (из корня проекта):

   ```bash
   python .test/scripts/gen_images.py
   ```

   Скрипт создаст 20 JPG-файлов в папке `images/`.

3. Запуск загрузчика (по умолчанию из .env UPLOADER_MODE=async):

   ```bash
   python main.py
   ```

   или явно через --mode:

   ```bash
   python main.py --mode sync
   python main.py --mode async
   ```
