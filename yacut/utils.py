from urllib.parse import unquote
import asyncio
import random
import string

import aiohttp

from . import app
from .models import URLMap

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
BASE_URL = f'{API_HOST}{API_VERSION}/disk/resources'
AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


def get_unique_short_id():
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


async def _make_request(endpoint, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{BASE_URL}/{endpoint}', headers=AUTH_HEADERS, params=params
        ) as response:
            data = await response.json()
            return data.get('href')


async def get_upload_link(filename):
    return await _make_request(
        'upload',
        {'path': f'app:/{filename}', 'overwrite': 'True'}  # noqa: E231
    )


async def get_download_link(file_path):
    return await _make_request(
        'download',
        {'path': file_path}
    )


async def upload_file_to_disk(file_data, filename):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            await get_upload_link(filename), data=file_data
        ) as response:
            location = response.headers.get('Location')
            if location:
                return unquote(location).replace('/disk', '')
            return None


async def upload_all_files(files):
    return await asyncio.gather(
        *[upload_file_to_disk(file.read(), file.filename) for file in files]
    )
