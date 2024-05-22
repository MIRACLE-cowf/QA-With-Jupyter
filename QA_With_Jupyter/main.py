from langchain_community.document_loaders import NotebookLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from CustomHelper.load_model import get_anthropic_model

loader = NotebookLoader(
	"./src/storm.ipynb",
	max_output_length=50,
	remove_newline=True
)

result = loader.load()
# print(result[0].page_content)


def pretty_print_notebook(notebook_str):

	# Split the string into individual cells based on cell type markers
	cells = notebook_str.strip().split("\n\n")
	full_content = ""
	for cell in cells:
		if cell.startswith("'markdown'"):
			# Extract and clean markdown content
			content = cell.split("cell: ")[1]
			content = content.replace("'['", "").replace("']'", "").replace("', '", "\n")
			full_content += content + "\n"

		elif cell.startswith("'code'"):
			# Extract and clean code content
			content = cell.split("cell: ")[1]
			content = content.replace("'['", "").replace("']'", "").replace("', '", "\n")
			code_content = "```python" + "\n" + content + "\n" + "```" + "\n"
			full_content += code_content
		full_content += "\n"

	return full_content


pretty_notebook = pretty_print_notebook(result[0].page_content)

qa_with_jupyter_prompt = ChatPromptTemplate.from_messages([
	("system", """You are a senior developer with many years of experience in the coding industry.

Now you have documents written in Jupyter Notebooks that look like this:

<jupyter_document>
{jupyter_document}
</jupyter_document>


Now your job is to take your time to read and analyze the documentation in that Jupyter notebook, and to respond to the user's questions."""),
	("human", "{input}")
])
llm = get_anthropic_model()
chain = (
	qa_with_jupyter_prompt.partial(jupyter_document=pretty_notebook)
	| llm
	| StrOutputParser()
)

for chunk in chain.stream({
	"input": "What is STORM Architecture?"
}):
	print(chunk, end="", flush=True)

