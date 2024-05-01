from llm_interfaces import Context, Form_groq, From_antropic, Agents
import os

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')

def clear_context() -> Context:
    clear_terminal()
    print("You've cleared the context")
    return Context()

def new_system_prompt() -> str:
    new = input("Type new system prompt: ")
    if len(new) < 5:
        print("Your new prompt was too short, at least 5 characters!")
        return new_system_prompt()
    print(f"Your new system prompt is {new}\n\n Heloo, how can i help you??\n")
    return new

def choose_agent():
    print(agetn_menu)
    while True:
        user_input = input("\nEnter the name of choosen agent: ")
        if user_input == "assistant":
            return Agents().assistant
        elif user_input == "reflector":
            return Agents().reflector
        else:
            print("Invalid agent name. Please try again.")

def choice_menu_logic():
    print(model_menu)
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




if __name__ == '__main__':

    main_menu = """
Welcome! What do you need to know boss?
\\q - Quit
\\a - Choose an agent you would like to converse wiht (default: assistant - normal chat)
\\c- Clear llms context
\\mc - Choose model AND clear context

\\menu or \\help -  these will print this menu

If you are using standard assistant agent you can specify these parameters:
\\s- Change system prompt (default: "You are a helpful assistant with a distinguished comedic sense.")
\\m- Choose chat model (default: lamma3-70B)

Enter your command or prompt:\n\n"""

    model_menu = """
Choose a chat model from the list below:
haiku (paid!)
sonnet (paid!)
opus (paid!)
llama3-8b
llama3-70b
llama2-70b
gemma-7B
mixtral-8x7B"""

    agetn_menu = """
Choose an Agent from the list below:
assistant (This is an ordinary chat. you can customize the system_prompt and choose a model) 
reflector (This is a double model; it generates one response and then reflects on it)
"""





    chat_log = Context()
    system_prompt = """You are a helpful assistant with a distinguished comedic sense."""
    model = Form_groq().llama3_70b
    agent = Agents().assistant

    user_prompt = input(main_menu)
    while True:
        if user_prompt == "\\q":
            print("Exiting the program...")
            break
        elif user_prompt == "\\mc":
            chat_log = clear_context()
            model = choice_menu_logic()
            user_prompt = input("\nWelcome! What do you need to know boss?\n")

        elif user_prompt == "\\m":
            model = choice_menu_logic()
            user_prompt = input("\nWelcome! What do you need to know boss?\n")

        elif user_prompt == "\\menu" or user_prompt == "\\help":
            user_prompt = input(main_menu)
        
        elif user_prompt == "\\a":
            agent = choose_agent()
            user_prompt = input("\nWelcome! What do you need to know boss?\n")

        elif user_prompt == "\\s":
            system_prompt = new_system_prompt()
            user_prompt = input("")

        elif user_prompt == "\\c":
            chat_log = clear_context()
            user_prompt = input("Type your first message:\n\n")

        elif user_prompt == "" or None:
            user_prompt = input("")
        else:
            chat_log = agent(system_prompt, user_prompt, chat_log, model)
            user_prompt = input("\n\n\n")