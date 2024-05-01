import os
import ast
import time
import anthropic
from groq import Groq
from dotenv import load_dotenv

class Context:
    '''This class provided you an easy way to create context chain'''
    def __init__(self) -> None:
        self.messages = []

    def add_system_message(self, system: str) -> None:
        self.messages.insert(0, {"role": "system", "content": f"{system}"})

    def add_user_message(self, prompt: str) -> None:
        self.messages.append({"role": "user", "content": f"{prompt}"})

    def add_assistant_message(self, response: str) -> None:
        self.messages.append({"role": "assistant", "content": f"{response}"},)
    
    def delete_last_message(self, num: int = 1) -> None:
        for i in range(num):
            self.messages.pop(-1)
    def delete_system_message(self) -> None:
        self.messages.pop(0)
    
    def get_last_message(self) -> dict[str, str]:
        '''{"role": "assistant", "content": f"{response}"}'''
        return self.messages[-1]
    
    def modify_last_message(self, new_message: str) -> None:
        last = self.get_last_message()
        self.delete_last_message()
        
        if last["role"] == "assistant":
            self.add_assistant_message(new_message)
        else:
            self.add_user_message(new_message)


    def to_list(self):
        return self.messages


class From_antropic:
    '''
    This class lets you choose form what antorpic
    models you want to recive response
    '''
    def __init__(self) -> None:
        load_dotenv()
        self.key = os.getenv("ANTROPIC_API")

    def send_request(self, system_prompt: str, context: list[dict], model: str) -> str:
        client = anthropic.Anthropic(
        api_key= self.key
        )
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=context
        )
        return message.content

    def haiku(self, system_prompt: str, context: list[dict]) -> str:
        return self.send_request(system_prompt, context, "claude-3-haiku-20240307")

    def sonnet(self, system_prompt: str, context: list[dict]) -> str:
        return self.send_request(system_prompt, context, "claude-3-sonnet-20240229")
    
    def opus(self, system_prompt: str, context: str) -> str:
        return self.send_request(system_prompt, context, "claude-3-opus-20240229")
    

class Form_groq:
    '''
    This class lets you choose what models
    (avelable at groq) you want to recive response
    '''
    def __init__(self) -> None:
        load_dotenv()
        self.key = os.getenv('GROQ')
        self.client = Groq(api_key=self.key)


    def send_request(self, system_prompt: str, user_prompt: str, context: Context, model: str, max_tokens: int, stream: bool) -> Context:
        context.add_system_message(system_prompt)
        context.add_user_message(user_prompt)
        
        if stream:
            text = ''
            stream = self.client.chat.completions.create(
                messages=context.to_list(),
                model=model,
                max_tokens=max_tokens,
                stream=True,
            )
            
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content != None:
                    text += content
                    print(content, end="")
            context.add_assistant_message(text)
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=context.to_list(), 
                max_tokens=max_tokens
            )
            context.add_assistant_message(response.choices[0].message.content)
        
        context.delete_system_message()
        return context


    def llama3_8b(self, system_prompt: str, user_prompt: str, context: Context, stream: bool = False) -> Context:
        return self.send_request(system_prompt, user_prompt, context, "llama3-8b-8192", 8192, stream)

    def llama3_70b(self, system_prompt: str, user_prompt: str, context: Context, stream: bool = False) -> Context:
        return self.send_request(system_prompt, user_prompt, context, "llama3-70b-8192", 8192, stream)
    
    def llama2_70b(self, system_prompt: str, user_prompt: str, context: Context, stream: bool = False) -> Context: 
        return self.send_request(system_prompt, user_prompt, context, "llama2-70b-4096", 4096, stream)

    def gemma_7B(self, system_prompt: str, user_prompt: str, context: Context, stream: bool = False) -> Context:
        return self.send_request(system_prompt, user_prompt, context, "gemma-7b-it", 8192, stream)

    def mixtral_8x7B(self, system_prompt: str, user_prompt: str, context: Context, stream: bool = False) -> Context: 
        return self.send_request(system_prompt, user_prompt, context, "mixtral-8x7b-32768", 32768, stream)


class Agents:
    '''This class lets you use agents that will perform a specific usecase'''
    def __init__(self) -> None:
        return

    def send_request_return_type(self, system_prompt:str, user_prompt: str, agent: str, return_type: type) -> type:
        '''This function ensures that the response is converted correctly to the desired type list, int, dict ect.
        There are 10 retries, if all of them fail, retuns None'''
        max_retries = 10
        attempts = 0
        while attempts < max_retries:
            try:
                # Sends a request to the groq api and checks if the response is a list
                response = ast.literal_eval(Form_groq().llama3_70b(system_prompt, [{"role": "user", "content": f"{user_prompt}"}]))
                if isinstance(response, return_type):
                    return response  
            except Exception as e:
                attempts += 1
                print(f"{agent} Attempt {attempts}/{max_retries} failed due to: {e}. Retrying in 2 seconds...")
                time.sleep(2)
        print(f"{agent} agent failed after maximum attempts")

    
    



    def assistant(self, system_prompt: str, user_prompt: str, contex:Context, model: Form_groq):
        '''
        This is a standard chat agent
        '''
        return model(system_prompt, user_prompt, contex, True)

 
    def reflector(self, user_prompt: str, context: Context) -> Context: 
        '''
        This is a reflector Agent he will generate a response and than reflect
        on it and agent will try to make a better one
        '''
        first_agent = """
        You are a helpful assistant.
        """
        new_context: Context = Form_groq().llama3_70b(first_agent, user_prompt, context)
        respone = new_context.get_last_message()["content"]

        new_context.delete_last_message()
        new_promp = (f"{new_context.get_last_message()["content"]} [assistant]{respone}[/assistant]")
        new_context.delete_last_message()

        out_agent = """
        You are an assistant refactor engine, you must read the assistant response and rewrite
        it and provide a more accurate one if needed. DON'T BE RESPOND WITH ANYTHING ELSE, JUST SEND THE REFACTORED RESPONDE
        """
        
        new_context = Form_groq().llama3_70b(out_agent, new_promp, new_context, True)
        respone = new_context.get_last_message()["content"]
        
        context.add_user_message(user_prompt)
        context.add_assistant_message(respone)
        return context
    
