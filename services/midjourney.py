import httpx
import json
import asyncio
from utils.db_api import create_image_query

class MJ:
    def __init__(self, token: str):
        self.base_url = 'https://api.useapi.net/v2/jobs/imagine'
        self.variation_url = "https://api.useapi.net/v2/jobs/button"
        self.check_url = "https://api.useapi.net/v2/jobs"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    async def async_get_variation_image(self, jobid: str, button_number: str):
        """Создай задачу по генерации вариаций картинки"""
        async with httpx.AsyncClient(timeout=300) as client_http:
            json_data = {
                "button": button_number,
                "jobid": jobid
            }
            response_task = await client_http.post(self.variation_url, headers=self.headers, json=json_data)
            result_task = json.loads(response_task.content)
            return result_task

    async def async_get_result_task(self, content: dict) -> dict:
        """Получи информацию о выполнении задачи"""
        async with httpx.AsyncClient(timeout=300) as client_http:
            response_task = await client_http.get(f'{self.check_url}/?jobid={content["jobid"]}',
                                         headers=self.headers)
            result_task = json.loads(response_task.content)
            return result_task

    async def async_generate_image(self, prompt: str):
        """Создай задачу по генерации картинки"""
        async with httpx.AsyncClient(timeout=300) as client_http:
            json_data = {
                "prompt": f"{prompt} --v 6.0"
            }
            response_task = await client_http.post(self.base_url, headers=self.headers, json=json_data)
            result_task = json.loads(response_task.content)
            return result_task