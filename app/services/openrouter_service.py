from __future__ import annotations

import requests

from app.core.config import settings
from app.core.logger import logger


class OpenRouterService:
    """
    Client for the OpenRouter Chat Completions API.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        headers = {
            "Authorization": (
                f"Bearer {settings.openrouter_api_key}"
            ),
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": settings.app_name,
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers "
                        "questions only using the provided context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
            "max_tokens": 800,
        }

        logger.info(
            "Calling OpenRouter model=%s",
            settings.openrouter_model,
        )

        try:
            response = requests.post(
                f"{settings.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )
        except requests.RequestException as exc:
            logger.exception(
                "Unable to connect to OpenRouter."
            )
            raise RuntimeError(
                "Unable to connect to OpenRouter."
            ) from exc

        logger.info(
            "OpenRouter HTTP %s",
            response.status_code,
        )

        try:
            data = response.json()
        except Exception as exc:
            logger.error(response.text)
            raise RuntimeError(
                "OpenRouter returned an invalid JSON response."
            ) from exc

        if not response.ok:
            logger.error(data)

            error = (
                data.get("error", {}).get("message")
                if isinstance(data, dict)
                else response.text
            )

            raise RuntimeError(
                f"OpenRouter error: {error}"
            )

        choices = data.get("choices")

        if not choices:
            logger.error(data)

            raise RuntimeError(
                "OpenRouter response does not contain choices."
            )

        message = choices[0].get("message", {})

        content = message.get("content")

        if not content:
            logger.error(data)

            raise RuntimeError(
                "OpenRouter returned an empty response."
            )

        return content.strip()