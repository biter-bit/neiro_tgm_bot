import httpx
import json
import asyncio

class MJ:
    def __init__(self, token: str):
        self.base_url = 'https://api.useapi.net/v2/jobs/imagine'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    async def async_create_image(self, json_data: dict, client_http: httpx.AsyncClient) -> dict:
        """Создай запрос на создание картинки"""
        response_task = await client_http.post(self.base_url, headers=self.headers, json=json_data)
        result_task = json.loads(response_task.content)
        return result_task

    async def async_get_result_task(self, content: dict, client_http: httpx.AsyncClient) -> dict:
        """Получи информацию о выполнении задачи"""
        response_task = await client_http.get(f'https://api.useapi.net/v2/jobs/?jobid={content["jobid"]}',
                                         headers=self.headers)
        result_task = json.loads(response_task.content)
        return result_task

    async def async_generate_image(self, prompt: str):
        """Создай картинку"""
        async with httpx.AsyncClient(timeout=300) as client_http:
            json_data = {
                "prompt": prompt
            }
            task = await self.async_create_image(json_data, client_http)

            while True:
                result_task = await self.async_get_result_task(task, client_http)
                if result_task['status'] in ['failed', "completed"]:
                    # response_image = await client.get(content_task['attachments'][0]['url'])
                    # image_stream = BytesIO(response_image.content)
                    # image = Image.open(image_stream)
                    # image.save("output_image.png")
                    return result_task
                await asyncio.sleep(5)
                continue