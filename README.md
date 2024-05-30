# Описание
Данный репозиторий представляет собой исходный код решения задачи распознавания именованных сущностей в рамках хакатона X5 Tech AI Hack, проводимого на платформе Codenrock с  17 по 30 мая 2024. 

По результатам хакатона было занято 8 место (команда DeepDeep). (F1 macro - 0,727 - public test, 0,599 - private test)

# Ход решения задачи:

1. Исследование данных
2. Аугментация данных и перевод исходной разметки в BIO формат
3. Тренировка трансформер-модели ru-Bert-base с замороженными эмбеддингами и частично замороженными слоями энкодера

# Структура проекта:

1. Каталог notebooks - jupiter-ноутбуки, в которых описан ход решения задачи
2. src - исходный код дополнительных функций (аугментация данных, BIO-разметка и др.)
3. Dockerfile - сборка проекта, запуск в контейнере и выполнение предсказаний для тестовой выборки через gitlab платформу, предоставленную Codenrock