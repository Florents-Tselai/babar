from babar import Extension
from typing import List

try:
    import llm
except ImportError:
    raise Exception(
        "You should `pip install llm`"
        "and probably some more models like `llm install llm-clip` . "
        "See https://llm.datasette.io/en/stable/plugins/directory.html#local-models"
    )


def llm_embed(text: str, model: str = "clip") -> List[float]:
    import llm

    embedding_model = llm.get_embedding_model(model)
    vector = embedding_model.embed(text)
    return vector


if __name__ == "__main__":
    Extension(
        "pgllm",
        llm_embed,
        comment="LLMs in postgres powered by Python LLM",
        default_version="0.1.0",
    )
