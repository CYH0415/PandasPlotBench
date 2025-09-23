from .openai_engine import OpenAIEngine
from .together_engine import TogetherEngine
from .openrouter_engine import OpenRouterEngine
from .custom_api_engine import CustomAPIEngine
from .custom2_api_engine import Custom2APIEngine


def get_model_by_name(
    model_name: str,
    model_pars: dict = {},
    system_prompt: str | None = None,
    **kwargs,
):
    kwargs.update(
        {
            "add_args": model_pars,
            "model_name": model_name,
        }
    )
    if system_prompt is not None:
        kwargs.update({"system_prompt": system_prompt})

    if model_name.startswith("openai/"):
        kwargs.update({"model_name": model_name[len("openai/") :]})
        model = OpenAIEngine(**kwargs)
    elif model_name.startswith("together/"):
        kwargs.update({"model_name": model_name[len("together/") :]})
        model = TogetherEngine(**kwargs)
    elif model_name.startswith("openrouter/"):
        kwargs.update({"model_name": model_name[len("openrouter/") :]})
        model = OpenRouterEngine(**kwargs)
    elif model_name.startswith("custom/"):
        kwargs.update({"model_name": model_name[len("custom/") :]})
        model = CustomAPIEngine(**kwargs)
    elif model_name.startswith("custom2/"):
        kwargs.update({"model_name": model_name[len("custom2/") :]})
        model = Custom2APIEngine(**kwargs)
    else:
        # That import is here temporary to prevent import of cuda-libraries if they are not needed.
        from .vllm_engine import VllmEngine

        model = VllmEngine(**kwargs)

    return model
