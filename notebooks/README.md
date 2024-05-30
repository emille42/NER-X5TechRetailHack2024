# Запуск ноутбуков:
Автор использовал Python 3.10.9 и Windows 10
1) Создать виртуальную среду окружения:  
**python -m venv .venv**
2) Активировать виртуальную среду окружения:  
**.\\.venv\Scripts\activate**
3) Установить зависимости:  
**python -m pip install -r requirements.txt**
4) Если используете CUDA, то в активированной виртуальной среде вводим:  
**python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118**