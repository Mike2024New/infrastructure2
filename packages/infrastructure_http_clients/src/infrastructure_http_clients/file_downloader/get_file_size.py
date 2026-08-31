import asyncio
import aiohttp


async def get_total_size(session: aiohttp.client.ClientSession, url: str, timeout: float = 10.0) -> int:
    """
    Получение размера файла в байтах.
    """
    try:
        async with session.head(url, timeout=timeout) as response:
            headers = response.headers
            if headers is None:
                return 0

        # попытка получить размер файла, если скачивается релиз с git
        if url.startswith(r'https://github.com/') and '/releases/' in url:
            async with session.head(headers.get('Location')) as response:
                headers = response.headers
                return int(headers.get('Content-Length', '0'))

        # попытка получить размер файла, если скачивается репозиторий с git (api ограничение на неавторизованные запросы 60/час)
        elif url.startswith(r'https://github.com/') and url.endswith('.zip'):
            try:
                owner, repo, *_ = url.split('https://github.com/')[-1].split('/')
                git_api_url = f'https://api.github.com/repos/{owner}/{repo}'
                async with session.get(git_api_url) as response:
                    data = await response.json()
                    total_size = data.get('size', 0)
                    total_size = total_size * 1024
                    return total_size
            except Exception:  # noqa
                return 0

        # если скачивается с hugging-face (через заголовок X-Linked-Size)
        elif url.startswith(r'https://huggingface.co/'):
            return int(headers.get('X-Linked-Size', '0'))
        # прочие случаи
        else:
            return int(headers.get('Content-Length', '0'))
    except Exception:  # noqa
        return 0


async def main():
    async with aiohttp.ClientSession() as session:
        total = await get_total_size(
            session=session,
            url='https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/vocabulary.txt',
        )
        print(total)


if __name__ == '__main__':
    asyncio.run(main())
