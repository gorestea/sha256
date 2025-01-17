# Асинхронное скачивание содержимого репозитория и вычисление SHA256 хэшей

Этот проект предоставляет скрипт для асинхронного скачивания содержимого репозитория и вычисления SHA256 хэшей файлов.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/gorestea/sha256
    cd sha256
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Использование

Запустите скрипт для скачивания содержимого репозитория и вычисления SHA256 хэшей:
```bash
python main.py
```

## Тестирование
Установите pytest-asyncio:

```bash
pip install pytest-asyncio
```
Запустите тесты с помощью pytest:

```bash
pytest
```

## Документация
<b>fetch_file</b>: Асинхронно скачивает файл по указанному URL и сохраняет его в указанное местоположение.

Параметры:
<ul>
session (aiohttp.ClientSession): Клиентская сессия aiohttp.

url (str): URL файла для скачивания.

dest (Path): Путь для сохранения скачанного файла.

</ul>
<b>fetch_repo_contents</b>: Асинхронно скачивает содержимое репозитория и сохраняет файлы в указанную директорию.

Параметры:

<ul>
repo_owner (str): Владелец репозитория.

repo_name (str): Имя репозитория.

dest_dir (Path): Директория для сохранения скачанных файлов.

</ul>
Возвращает: List[Path]: Список путей к сохраненным файлам.

<b>calculate_sha256</b>: вычисляет SHA256 хэш файла.

Параметры: file_path (Path): Путь к файлу.

Возвращает: str: SHA256 хэш файла в виде шестнадцатеричной строки.


<b>ОТВЕТЫ</b>:
1. Как вы реализовали асинхронное выполнение задач в вашем скрипте?
   
   aiohttp + asyncio


2. Какие библиотеки использовались для скачивания содержимого репозитория и для каких целей?

   aiohttp (для асинхронных http запросов) + aiofiles (асинхронная работа с файлами)


3. Какие проблемы асинхронности вы сталкивались при выполнении задания и как их решали?

   С проблемами по решению задачи не столкнулся, а столкнулся с проблемами с nitpick

4. Как вы организовали скачивание файлов во временную папку?

   aiofiles + from from tempfile import TemporaryDirectory для создания временной папки

5. Какие основные требования wemake-python-styleguide вы находите наиболее важными для поддержания качества кода?

   Явное использование всех импортов, лучшая читаемость кода за счет ограничения вложенности

6. Как вы настраивали свой проект для соответствия конфигурации nitpick, указанной в задании? Были ли трудности при настройке?

   С этим возникли сложности. По flake8 у меня код проходит, но при обращении к стилям репозитория https://gitea.radium.group/radium/project-configuration/ для nitpick я получаю ошибку 
```bash
has an incorrect style. Invalid TOML (toml.decoder.TomlDecodeError: Found invalid character in key name: '!'. Try quoting the key name. (line 1 column 2 char 1))
```

7. Какие инструменты использовали для измерения 100% покрытия тестами?

   coverage. Я добился покрытия тестами 81%. Непокрытой осталась лишь функция main, которая собирает в себе все функции, которые прошли проверку

8. Какие типы тестов вы написали для проверки функциональности вашего скрипта? (Например, модульные тесты, интеграционные тесты)

   Модульные тесты проверяют отдельные функции, такие как calculate_sha256.
   
   Интеграционные тесты проверяют функции, работающие с внешними ресурсами, такие как fetch_file и fetch_repo_contents.

9. Как вы тестировали асинхронный код? Использовали ли вы моки (mocks) или стабы (stubs) для тестирования асинхронных операций?

   pytest-asyncio. Использовал моки aioresponses, для имитации ответов от внешних HTTP-запросов
