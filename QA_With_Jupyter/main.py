from langchain_community.chat_message_histories import ChatMessageHistory
from load_file import run_load_file
from qa_chain import get_qa_chain


if __name__ == '__main__':
	data = run_load_file("./src/")
	qa_chain = get_qa_chain(data)
	chat_history = ChatMessageHistory()
	while True:

		user_input = input("Question: ")

		if user_input == "q":
			print("Bye Bye")
			break

		ai_message = ""
		for chunk in qa_chain.stream({
			"input": user_input,
			"chat_history": chat_history.messages,
		}):
			ai_message += chunk
			print(chunk, end="", flush=True)

		print("\n")
		chat_history.add_user_message(user_input)
		chat_history.add_ai_message(ai_message)


