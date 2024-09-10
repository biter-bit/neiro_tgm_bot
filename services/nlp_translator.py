from aiohttp import ClientSession
from requests import Session

class Translator:
    def __init__(self, token, proxy):
        self.proxy = proxy
        self.proxies_dict = {"http": proxy, "https": proxy}
        self.url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com",
        }

    async def async_translate(self, text: str, to_: str = "en", from_: str = "ru") -> dict:
        payload = {"text": text, "to": to_, "from": from_}

        async with ClientSession(headers=self.headers) as session:
            async with session.post(url=self.url, data=payload, proxy=self.proxy) as response:
                if response.ok:
                    result = await response.json()
                    translation = result.get("translated_text").get(to_)
                    if not translation:
                        return {"status": "error", "result": f"TRANSLATION ERROR | {await response.text()}"}
                    return {"status": "ok", "result": translation}
                else:
                    return {"status": "error", "result": f"TRANSLATION ERROR | {await response.text()}"}

    def translate(self, text: str, to_: str = "en", from_: str = "ru") -> str | None:
        payload = {"text": text, "to": to_, "from": from_}

        with Session() as session:
            response = session.post(url=self.url, data=payload, headers=self.headers, proxies=self.proxies_dict)
            if response.ok:
                result = response.json()
            else:
                return

        translation = result.get("translated_text").get(to_)

        if translation:
            return translation

        return