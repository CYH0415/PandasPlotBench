import os
from .base_engine import BaseOpenAIEngine, BaseOpenAIImageEngine
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


class Custom2APIEngine(BaseOpenAIImageEngine, BaseOpenAIEngine):
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
        # 使用CUSTOM2_API_KEY作为API密钥环境变量名
        api_key_name = "CUSTOM2_API_KEY"
        super().__init__(
            model_name, system_prompt, add_args, wait_time, attempts, api_key_name
        )
        self.name = "custom2/" + model_name
        # 直接在代码中设置API URL
        self.model_url = "http://162.251.95.230:46333/v1"
        
        self.tokens_highlighted = tokens_highlighted