import os
from .base_engine import BaseOpenAIEngine, BaseOpenAIImageEngine
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


class CustomAPIEngine(BaseOpenAIImageEngine, BaseOpenAIEngine):
    def __init__(
        self,
        model_name,
        system_prompt: str = "You are helpful assistant",
        do_logprobs: bool = False,
        tokens_highlighted: list[str] = [],
        add_args: dict = {},
        wait_time: float = 20.0,
        attempts: int = 10,
    ) -> None:
        # 使用CUSTOM_API_KEY作为API密钥环境变量名
        api_key_name = "CUSTOM_API_KEY"
        super().__init__(
            model_name, system_prompt, add_args, wait_time, attempts, api_key_name
        )
        self.name = "custom/" + model_name
        # 直接在代码中设置API URL
        self.model_url = "http://10.130.136.14:49382/v1/chat/completions"
        
        self.tokens_highlighted = tokens_highlighted