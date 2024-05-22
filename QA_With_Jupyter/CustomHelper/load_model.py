import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

def get_anthropic_model(model_name="haiku", temperature=0.3) -> ChatAnthropic:
    """Load the Anthropic model easily. You can freely revise it to make it easier to use."""
    if model_name == 'sonnet':
        model = "claude-3-sonnet-20240229"
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