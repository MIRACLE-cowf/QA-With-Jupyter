from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from CustomHelper.load_model import get_anthropic_model, get_openai_model


def get_qa_chain(pretty_notebook: str):
	"""Basic and Simple QA Chain using LangChain"""
	qa_with_jupyter_prompt = ChatPromptTemplate.from_messages([
		("system", """You are a senior developer with many years of experience in the coding industry.

Now you have documents written in Jupyter Notebooks that look like this:

<jupyter_document>
{jupyter_document}
</jupyter_document>


Now your job is to take your time to read and analyze the documentation in that Jupyter notebook, and to respond to the user's questions."""),
		MessagesPlaceholder("chat_history"),
		("human", "{input}")
	])

	llm = get_anthropic_model(model_name="sonnet") # change model name if you want to use more intelligence claude model (haiku, sonnet, opus)
	# llm = get_openai_model() # change this 'get_openai_model()' if you want to use OpenAI model

	fallback_llm = llm.with_fallbacks([llm] * 5)

	qa_chain = (
		qa_with_jupyter_prompt.partial(jupyter_document=pretty_notebook)
		| fallback_llm
		| StrOutputParser()
	)
	return qa_chain