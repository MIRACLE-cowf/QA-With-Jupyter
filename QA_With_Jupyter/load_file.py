import os

from langchain_community.document_loaders import NotebookLoader


def _get_ipynb_files(directory):
	"""Get all ipynb files from a given directory.(src)"""
	ipynb_list = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.endswith(".ipynb"):
				ipynb_list.append(file.strip(".ipynb"))
	return ipynb_list


def _display_file_list(file_list: list):
	"""Display a list of ipynb files"""
	if len(file_list) > 0:
		print(f"There are {len(file_list)} files in the list:")
		for index, file in enumerate(file_list, start=1):
			print(f"{index}. {file}.ipynb")
	else:
		print("The file list is empty")


def _get_user_selection(file_list: list):
	"""Get user selection from a list of ipynb files"""
	while True:
		try:
			selected_index = int(input("Enter the index of the file to load: "))
			if 1<= selected_index <= len(file_list):
				return file_list[selected_index - 1]
			else:
				print("Invalid index. Please try again.")
		except ValueError:
			print("Invalid index. Please try again.")


def _load_notebook(file_path):
	"""Load an ipynb file using LangChain NotebookLoader"""
	loader = NotebookLoader(
		file_path+".ipynb",
		max_output_length=50,
		remove_newline=True
	)
	return loader.load()


def _pretty_print_notebook(notebook_str):
	"""Transform raw data to pretty content"""

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


def run_load_file(file_path):
	"""Run all functions to load ipynb files"""
	ipynb_list = _get_ipynb_files(file_path)
	_display_file_list(ipynb_list)

	if ipynb_list:
		selected_ipynb = _get_user_selection(ipynb_list)
		file_path = os.path.join(file_path, selected_ipynb)
		notebook_data = _load_notebook(file_path)
		notebook_str = _pretty_print_notebook(notebook_data[0].page_content)
		return notebook_str
	else:
		print("There is no ipynb file in src")