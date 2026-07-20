from urllib.parse import unquote
import asyncio

import aiohttp

from . import app

BASE_URL = (
    f'{app.config["API_HOST"]}'
    f'{app.config["API_VERSION"]}/disk/resources'
)
UPLOAD_URL = f'{BASE_URL}/upload'
DOWNLOAD_URL = f'{BASE_URL}/download'
AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
UPLOAD_ERROR_TEMPLATE = 'Не удалось загрузить файл {}'


async def _make_request(endpoint, params):
    if endpoint == 'upload':
        url = UPLOAD_URL
    else:
        url = DOWNLOAD_URL
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers=AUTH_HEADERS, params=params
        ) as response:
            return (await response.json()).get('href')


async def upload_file_to_disk(file_data, filename):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            await _make_request(
                'upload',
                {'path': f'app:/{filename}', 'overwrite': 'True'}  # noqa: E231
            ),
            data=file_data
        ) as response:
            return unquote(
                response.headers.get('Location')
            ).replace('/disk', '')


def upload_all_files(files):
    async def _upload_all():
        results = []
        for file in files:
            filename = file.filename
            location = await upload_file_to_disk(file.read(), filename)
            if not location:
                raise RuntimeError(UPLOAD_ERROR_TEMPLATE.format(filename))
            results.append(await _make_request('download', {'path': location}))
        return results
    return asyncio.run(_upload_all())
