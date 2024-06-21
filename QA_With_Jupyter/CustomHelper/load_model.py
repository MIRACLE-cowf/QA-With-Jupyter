import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()


def get_anthropic_model(model_name="haiku", temperature=0.3) -> ChatAnthropic:
    """Load the Anthropic model easily."""
    if model_name == 'sonnet':
        model = "claude-3-5-sonnet-20240620"
    elif model_name == 'haiku':
        model = "claude-3-haiku-20240307"
    else:
        model = "claude-3-opus-20240229"

    llm = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=4096,
        anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        default_headers={"anthropic-beta": "tools-2024-05-16"}
    )
    return llm


def get_openai_model(temperature=0.3) -> ChatOpenAI:
    llm = ChatOpenAI(
        model_name="gpt-4o-2024-05-13",
        temperature=temperature,
        max_tokens=4096,
        openai_api_key=os.getenv('OPENAI_API_KEY'),
    )
    return llm