import hashlib
import aiofiles
import aiohttp
import pytest
from aioresponses import aioresponses
from pathlib import Path
from tempfile import TemporaryDirectory
from main import calculate_sha256, fetch_file, fetch_repo_contents


@pytest.mark.asyncio
async def test_fetch_file():
    """
    Тест асинхронной функции fetch_file.

    Проверяет, что функция правильно загружает содержимое файла
    и сохраняет его по указанному пути.
    """
    url = "https://example.com/testfile"
    content = b"Test content"
    with aioresponses() as m:
        m.get(url, body=content)

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "testfile"
            async with aiohttp.ClientSession() as session:
                await fetch_file(session, url, temp_path)

            async with aiofiles.open(temp_path, "rb") as f:
                result = await f.read()

            assert result == content


@pytest.mark.asyncio
async def test_fetch_repo_contents():
    """
    Тест асинхронной функции fetch_repo_contents.

    Проверяет, что функция правильно загружает список файлов из репозитория
    и сохраняет их по указанным путям.
    """
    repo_owner = "radium"
    repo_name = "project-configuration"
    contents_url = (f"https://gitea.radium.group/api/v1/repos/"
                    f"{repo_owner}/{repo_name}/contents")
    files_list = [
        {"type": "file", "name": "file1.txt",
         "download_url": "https://example.com/file1.txt"},
        {"type": "file", "name": "file2.txt",
         "download_url": "https://example.com/file2.txt"},
    ]

    with aioresponses() as m:
        m.get(contents_url, payload=files_list)
        m.get("https://example.com/file1.txt", body=b"Content of file1")
        m.get("https://example.com/file2.txt", body=b"Content of file2")

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            downloaded_files = await fetch_repo_contents(
                repo_owner, repo_name, temp_path)

            assert (temp_path / "file1.txt").exists()
            assert (temp_path / "file2.txt").exists()
            assert len(downloaded_files) == 2


def test_calculate_sha256():
    """
    Тест функции calculate_sha256.

    Проверяет, что функция правильно вычисляет SHA256 хэш файла.
    """
    content = b"Test content for hashing"
    expected_hash = hashlib.sha256(content).hexdigest()

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "testfile"
        with open(temp_path, "wb") as f:
            f.write(content)

        result = calculate_sha256(temp_path)
        assert result == expected_hash
