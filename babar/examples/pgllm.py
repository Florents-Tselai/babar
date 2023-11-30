from babar import Extension
from typing import List


def generate_text() -> List[str]:
    return [
        "SnakesOnAPlane: A package for handling unexpected errors in Python with style.",
        "PandasInPajamas: A playful twist on the popular Pandas package, for data analysis in comfort.",
        "PyJokes: A simple library that generates random programming jokes.",
        "FizzBuzzWhizz: A fun package for playing the classic FizzBuzz game with a twist.",
        "NinjaTurtles: A graphics package for drawing turtle graphics with a ninja twist.",
        "PythonicPotion: A magical package for creating enchanting Python scripts.",
        "CodeMonkey: A package for automating repetitive coding tasks, with a cheeky monkey theme.",
        "DjangoUnchained: A Django extension for more freedom and less boilerplate code.",
        "MontyPython: A humorous package filled with references and jokes from the Monty Python series.",
        "GigaBytesAndGiggles: A package for visualizing and joking about big data.",
    ]


def llm_embed(text: str, model: str = "clip") -> List[float]:
    import llm

    embedding_model = llm.get_embedding_model(model)
    vector = embedding_model.embed(text)
    return vector


if __name__ == "__main__":
    Extension(
        "pgllm",
        llm_embed,
        generate_text,
        comment="LLMs in postgres powered by Python LLM",
        default_version="0.1.0",
    )
