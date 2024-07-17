import asyncio
import hashlib
import tempfile
from pathlib import Path
from typing import List
import aiofiles
import aiohttp


async def fetch_file(
        session: aiohttp.ClientSession, url: str, dest: Path) -> None:
    """
    Асинхронно скачивает файл по указанному URL и сохраняет его
    в указанное местоположение.

    :param session: Клиентская сессия aiohttp.
    :param url: URL файла для скачивания.
    :param dest: Путь для сохранения скачанного файла.
    """
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        async with aiofiles.open(dest, "wb") as f:
            await f.write(content)


async def fetch_repo_contents(
        repo_owner: str, repo_name: str, dest_dir: Path) -> List[Path]:
    """
    Асинхронно скачивает содержимое репозитория и сохраняет файлы
    в указанную директорию.

    :param repo_owner: Владелец репозитория.
    :param repo_name: Имя репозитория.
    :param dest_dir: Директория для сохранения скачанных файлов.
    :return: Список путей к сохраненным файлам.
    """
    contents_url = (f"https://gitea.radium.group/api/v1/repos/"
                    f"{repo_owner}/{repo_name}/contents")
    async with aiohttp.ClientSession() as session:
        async with session.get(contents_url) as response:
            response.raise_for_status()
            files = await response.json()

        tasks = []
        for file in files:
            if file["type"] == "file":
                file_url = file["download_url"]
                dest_file = dest_dir / file["name"]
                tasks.append(fetch_file(session, file_url, dest_file))

        await asyncio.gather(*tasks)

        return [dest_dir / file["name"] for file in files
                if file["type"] == "file"]


def calculate_sha256(file_path: Path) -> str:
    """
    Вычисляет SHA256 хэш файла.

    :param file_path: Путь к файлу.
    :return: SHA256 хэш файла в виде шестнадцатеричной строки.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


async def main() -> None:
    """
    Основная функция, скачивающая содержимое репозитория
    и выводящая SHA256 хэши каждого файла.
    """
    repo_owner = "radium"
    repo_name = "project-configuration"
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        downloaded_files = await fetch_repo_contents(
            repo_owner, repo_name, temp_path)

        for file_path in downloaded_files:
            print(f"{file_path}: {calculate_sha256(file_path)}")


if __name__ == "__main__":
    asyncio.run(main())
