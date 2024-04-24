from llms import context,  llm_interfaces
from rich import print
from rich.console import Console
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.prompt import Prompt
import py


def clear_context():
    print(f"\033[1m You've cleared the context: \033[0m")
    return context.context


def chat(system_prompt: str, user_prompt: str, chat_log: context.context, model):
    chat_log.add_user_message(user_prompt)
    response = model(system_prompt, chat_log.to_list())
    chat_log.add_assistant_message(response)
    return response



def choice_menu_logic():
    while True:
            c.print(model_menu)
            user_input = input("\n")
            if user_input == "haiku":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.from_antropic().haiku
                
            elif user_input == "sonnet":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.from_antropic().sonnet

            elif user_input == "opus":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.from_antropic().opus
                
            elif user_input == "llama3-8b":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.form_groq().llama3_8b

            elif user_input == "llama3-70b":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.form_groq().llama3_70b
            elif user_input == "llama2-70b":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")
                return llm_interfaces.form_groq().llama2_70b
                
            elif user_input == "gemma-7B":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.form_groq().gemma_7B
                
            elif user_input == "mixtral-8x7B":
                c.print(f"\nYou are using {user_input} have fun!!", style="bold magenta")

                return llm_interfaces.form_groq().mixtral_8x7B
                
            else:
                c.print(f"Invalid model name. Please try again.", style="bold red")



main_menu = """
[menu_title]Welcome! What do you need to know boss?[/menu_title]        
[option]\\q[/option] - Quit
[option]\\s[/option] - Change system prompt default "Provide brief and precise answers. Elaborate only if requested."
[option]\\m[/option] - Choose chat model default lamma3-70B
[option]\\c[/option] - Clear llms context
[option]\\mc[/option] - Choose model AND clear context
Enter your command:
"""

model_menu = """
[menu_title]Choose a chat model from the list below:[/menu_title]
[paid_model]haiku (paid!)[/paid_model]
[paid_model]sonnet (paid!)[/paid_model]
[paid_model]opus (paid!)[/paid_model]
[model_name]llama3-8b[/model_name]
[model_name]llama3-70b[/model_name]
[model_name]llama2-70b[/model_name]
[model_name]gemma-7B[/model_name]
[model_name]mixtral-8x7B[/model_name]
[input_prompt]Enter the model name:[/input_prompt] """



custom_theme = Theme({
    "menu_title": "bold magenta",
    "model_name": "bold cyan",
    "paid_model": "bold yellow",
    "input_prompt": "bold magenta",
    "default": "italic",
    "menu_title": "bold magenta",
    "option": "bold cyan",
    "command": "green",
    "default": "italic"
})
c = py.Console()


system_prompt = "You are a helpfull assistan with a BRO personality, style you response in mark up but not indide code blocks"
chat_log = context.context()
model = llm_interfaces.form_groq().llama3_70b

c.print(main_menu)
user_prompt = input()

while True:
    if user_prompt == "\\q":
        print("Exiting the program...")
        break
    elif user_prompt == "\\mc":
        chat_log = clear_context()
        model = choice_menu_logic()
        c.print("\nWelcome! what do you need to know boss?\n", style= "#408000")
        user_prompt = input("")

    elif user_prompt == "\\m":
        model = choice_menu_logic()
        c.print("\nWelcome! what do you need to know boss?\n", style= "#408000")
        user_prompt = input("")

    elif user_prompt == "\\c":
        chat_log = context.context()
        c.print("Type your first message:\n", style= "bold magenta")
        user_prompt = input("")

    elif user_prompt == "" or None:
        user_prompt = input("")

    else:
        c.print(Markdown(chat(system_prompt, user_prompt, chat_log, model)), style= "#408000")
        user_prompt = input("\n")