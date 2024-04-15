# Dear Diary

## Описание
Приложение дневника на DRF


## Установка
1. Клонируйте.
2. Соберите докер контейнер:

`cd ./.devcontainer \`

`docker build  \`

`docker run -p 8080:8080 project-name`

## Celery
Для запуска celery на Windows необходимо выполнить следующие команды:


`python -m celery -A  diary_app worker -E  --pool solo`

`python -m celery -A  diary_app beat -E `

Без `--pool solo` выполнение задач на Windows может не работать

