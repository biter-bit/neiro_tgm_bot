import httpx
import json


class MJ:
    def __init__(self, token: str):
        self.base_url = 'https://api.useapi.net/v2/jobs/imagine'
        self.variation_url = "https://api.useapi.net/v2/jobs/button"
        self.check_url = "https://api.useapi.net/v2/jobs"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        self.result = {
            "status_code": None,
            "result": None
        }

    async def _make_request(self, method: str, url: str, json_data: dict = None, params: dict = None) -> dict:
        """Выполнить HTTP-запрос и обработать ошибки."""
        try:
            async with httpx.AsyncClient(timeout=120) as client_http:
                if method == "POST":
                    response = await client_http.post(url, headers=self.headers, json=json_data)
                elif method == "GET":
                    response = await client_http.get(f'{self.check_url}/?jobid={params["jobid"]}', headers=self.headers, params=params)
                response.raise_for_status()
                result_task = response.json()  # Преобразуем ответ в JSON
                return {
                    "status_code": result_task["code"],
                    "result": result_task
                }
        except httpx.HTTPStatusError as e:
            return {
                "status_code": e.response.status_code,
                "result": e.response.text
            }
        except httpx.TimeoutException:
            return {
                "status_code": 408,  # Тайм-аут
                "result": "Запрос превышает время ожидания"
            }
        except httpx.RequestError as e:
            return {
                "status_code": 500,  # Общая ошибка запроса
                "result": str(e)
            }
        except json.JSONDecodeError:
            return {
                "status_code": 500,  # Ошибка декодирования JSON
                "result": "Ошибка декодирования JSON"
            }

    async def async_get_variation_image(self, jobid: str, button_number: str) -> dict:
        """Создать задачу по генерации вариаций картинки."""
        json_data = {
            "button": button_number,
            "jobid": jobid
        }
        return await self._make_request("POST", self.variation_url, json_data=json_data)

    async def async_get_result_task(self, content: dict) -> dict:
        """Получить информацию о выполнении задачи."""
        params = {"jobid": content["jobid"]}
        return await self._make_request("GET", self.check_url, params=params)

    async def async_generate_image(self, prompt: str) -> dict:
        """Создать задачу по генерации картинки."""
        json_data = {
            "prompt": f"{prompt} --v 6.0"
        }
        return await self._make_request("POST", self.base_url, json_data=json_data)