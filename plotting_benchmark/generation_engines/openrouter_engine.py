import warnings
import os
from .base_engine import BaseOpenAIEngine, BaseOpenAIImageEngine
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


class OpenRouterEngine(BaseOpenAIImageEngine, BaseOpenAIEngine):
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
        # 使用QWEN_KEY作为API密钥
        api_key_name = "QWEN_KEY"
        super().__init__(
            model_name, system_prompt, add_args, wait_time, attempts, api_key_name
        )
        self.name = "openrouter/" + model_name
        self.model_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # 添加OpenRouter特定的headers
        api_key = os.getenv(api_key_name)
        self.headers.update({
            "HTTP-Referer": "https://github.com/JetBrains-Research/PandasPlotBench",
            "X-Title": "PandasPlotBench"
        })
        
        if do_logprobs:
            # OpenRouter可能不支持logprobs，这里可以忽略或警告
            warnings.warn("OpenRouter may not support logprobs feature")
        
        self.tokens_highlighted = tokens_highlighted
