from urllib.parse import unquote
import asyncio

import aiohttp

from settings import Config

BASE_URL = f'{Config.API_HOST}{Config.API_VERSION}/disk/resources'
UPLOAD_URL = f'{BASE_URL}/upload'
DOWNLOAD_URL = f'{BASE_URL}/download'
AUTH_HEADERS = {'Authorization': f'OAuth {Config.DISK_TOKEN}'}
UPLOAD_ERROR_TEMPLATE = 'Не удалось загрузить файл {}'


async def _make_request(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers=AUTH_HEADERS, params=params
        ) as response:
            return (await response.json()).get('href')


async def upload_file_to_disk(file_data, filename):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            await _make_request(
                UPLOAD_URL,
                {'path': f'app:/{Config.DISK_FOLDER}/{filename}',  # noqa: E231
                    'overwrite': 'True'}
            ),
            data=file_data
        ) as response:
            return unquote(
                response.headers.get('Location')
            ).replace('/disk', '')


def upload_all_files(files):
    async def _upload_all():
        return await asyncio.gather(*[
            _make_request(DOWNLOAD_URL, {'path': location})
            for location in await asyncio.gather(*[
                upload_file_to_disk(file.read(), file.filename)
                for file in files
            ])
        ])
    return asyncio.run(_upload_all())
