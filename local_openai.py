import os
from langchain_openai import ChatOpenAI


class ChatOpenAI_mock(ChatOpenAI):
    """Connect LangChain to LM Studio."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "base_url",
            os.getenv(
                "LM_STUDIO_BASE_URL",
                "http://192.168.10.2:1234/"
            )
        )
        kwargs.setdefault(
            "api_key",
            os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        )
        super().__init__(*args, **kwargs)