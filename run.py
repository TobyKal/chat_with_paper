from llm_interfaces import Context, Form_groq, From_antropic, Agents
import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')

def clear_context() -> Context:
    clear_terminal()
    print("You've cleared the context:")
    return Context()

def new_system_prompt() -> str:
    new = input("Type new system prompt:\n")
    if len(new) < 5:
        print("Your new prompt was too short, at least 5 characters!\n")
        return new_system_prompt()
    print(f"Your new system prompt is {new}\n\n Heloo, how can i help you??\n")
    return new

def chat(user_prompt: str, chat_log: Context) -> str:
    chat_log.add_user_message(user_prompt)
    response = Agents().thinker(chat_log.to_list())
    print(response)
    chat_log.delete_last_message()
    new = f"[user]{user_prompt}[/user][thinking]{response}[/thinking][response]"
    chat_log.add_user_message(new)
    response = Agents().responder(chat_log.to_list())
    chat_log.add_assistant_message(response)
    return response

def choice_menu_logic():
    while True:
        user_input = input("\nEnter the model name: ")
        if user_input == "haiku":
            return From_antropic().haiku
        elif user_input == "sonnet":
            return From_antropic().sonnet
        elif user_input == "opus":
            return From_antropic().opus
        elif user_input == "llama3-8b":
            return Form_groq().llama3_8b
        elif user_input == "llama3-70b":
            return Form_groq().llama3_70b
        elif user_input == "llama2-70b":
            return Form_groq().llama2_70b
        elif user_input == "gemma-7B":
            return Form_groq().gemma_7B
        elif user_input == "mixtral-8x7B":
            return Form_groq().mixtral_8x7B
        else:
            print("Invalid model name. Please try again.")


main_menu = """
Welcome! What do you need to know boss?[/menu_title]        
\\q - Quit
\\s- Change system prompt default "Provide brief and precise answers. Elaborate only if requested."
\\m- Choose chat model default lamma3-70B
\\c- Clear llms context
\\mc - Choose model AND clear context
Enter your command:
"""

model_menu = """
Choose a chat model from the list below:[/menu_title]
haiku (paid!)
sonnet (paid!)
opus (paid!)
llama3-8b
llama3-70b
llama2-70b
gemma-7B
mixtral-8x7B

Enter the models name """

chat_log = Context()
system_prompt = """You are a proactive and helpful assistant. provide answers to questions or to carry out the tasks efficiently.
"""
model = Form_groq().llama3_70b

print(main_menu)
user_prompt = input()

while True:
    if user_prompt == "\\q":
        print("Exiting the program...")
        break
    elif user_prompt == "\\mc":
        chat_log = clear_context()
        model = choice_menu_logic()
        print("\nWelcome! What do you need to know boss?\n")
        user_prompt = input("")

    elif user_prompt == "\\m":
        model = choice_menu_logic()
        print("\nWelcome! What do you need to know boss?\n")
        user_prompt = input("")
    
    elif user_prompt == "\\s":
        system_prompt = new_system_prompt()
        user_prompt = input("")

    elif user_prompt == "\\c":
        chat_log = clear_context()
        print("Type your first message:\n")
        user_prompt = input("")

    elif user_prompt == "" or None:
        user_prompt = input("")
    else:
        print("\n", chat(user_prompt, chat_log))
        user_prompt = input("\n\n")