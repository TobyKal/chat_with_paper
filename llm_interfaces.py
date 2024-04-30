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

    def add_user_message(self, prompt: str, person: str = "") -> None:
        '''Add user prompt to context, you can specify person like this
        person = "Toby: " This let's llm idntifie the user.'''
        self.messages.append({"role": "user", "content": f"{person}{prompt}"})

    def add_assistant_message(self, response: str) -> None:
        self.messages.append({"role": "assistant", "content": f"{response}"},)
    
    def delete_last_message(self, num: int = 1) -> None:
        '''Pops last send messages, user and assistant'''
        for i in range(num):
            self.messages.pop(-1)

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

    def send_streaming_request(self, system_prompt: str, context: list[dict], model: str, max_tokens: int):       
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        text = ''
        stream = self.client.chat.completions.create(
            messages=context,
            model=model,
            max_tokens=max_tokens,
            stream=True,
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content != None:
                text += content
                print(content, end="")
        return text


    def send_request(self, system_prompt: str, context: list[dict], model: str, max_tokens: int) -> str:
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        

        response = self.client.chat.completions.create(
            model=model,
            messages=context, 
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


    def llama3_8b(self, system_prompt: str, context: list[dict], stream: bool = False) -> str:
        if stream:
            return self.send_streaming_request(system_prompt, context, "llama3-8b-8192", 8192)
        else:
            return self.send_request(system_prompt, context, "llama3-8b-8192", 8192)

    def llama3_70b(self, system_prompt: str, context: list[dict], stream: bool = False) -> str:
        if stream:
            return self.send_streaming_request(system_prompt, context, "llama3-70b-8192", 8192)
        else:
            return self.send_request(system_prompt, context, "llama3-70b-8192", 8192)
    
    def llama2_70b(self, system_prompt: str, context: list[dict], stream: bool = False) -> str:
        if stream:
            return self.send_streaming_request(system_prompt, context, "llama2-70b-4096", 4096)
        else:    
            return self.send_request(system_prompt, context, "llama2-70b-4096", 4096)

    def gemma_7B(self, system_prompt: str, context: list[dict], stream: bool = False) -> str:
        if stream:
            return self.send_streaming_request(system_prompt, context, "gemma-7b-it", 8192)
        else:
            return self.send_request(system_prompt, context, "gemma-7b-it", 8192)

    def mixtral_8x7B(self, system_prompt: str, context: list[dict], stream: bool = False) -> str:
        if stream:
            return self.send_streaming_request(system_prompt, context, "mixtral-8x7b-32768", 32768)
        else:    
            return self.send_request(system_prompt, context, "mixtral-8x7b-32768", 32768)


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
    

    def extractor(self, text: str) -> list[str]:
        '''This agent is focused on EXTRACTING noteworthy informations
        from a supplied text and returns a list of stings with infromations
        if all of the tries fail, it will return an empty list'''

        system_prompt = """You are an advanced algorithm that specializes in
        retrieving noteworthy information for text supplied by the user. 
        You are only allowed to respond in the form of a Python list of strings, 
        where each string should contain information from one distinct topic.
        YOU ARE NOT ALLWED TO RESPOND IN ANY OTHER WAY EXCEPT PYTHON LIST"""

        response = self.send_request_return_type(system_prompt, text, "Extractor", list)
        if response == None: return []
        return response 
    
    def question_asker(self, text: str) -> list[str]:
        '''
        This agent is focused on creating QUESTIONS THAT ANSWER CAN BE FOUND
        in a supplied text and returns a list of stings with infromations
        if all of the tries fail, it will return an empty list
        '''

        system_prompt = """You are an advanced algorithm that specializes in
        creating questions, form a recived information, answers to with you can
        find in that infrmation. you are only allowed to respond in the form of a Python list of strings, 
        where each string should contain a question do not repeate questions.
        YOU ARE NOT ALLWED TO RESPOND IN ANY OTHER WAY EXCEPT PYTHON LIST"""

        response = self.send_request_return_type(system_prompt, text, "Question_asker", list)
        if response == None: return []
        return response 
    
    def thinker(self, context: Context) -> list[str]:
        '''
        This agent is focused on THINKING this agent will will think about your prompt
        it will try to figure out how to respond to your quesion.
        '''
        system_prompt = """
        You are a large language model. You will be provided a user message.
        I want you to analyze that message and do 'thinking' about it, think about what the user meant,
        and how could you respond to it, be dense, short and practical with your thoughts. YOU ARE A THINKER, DO NOT ANSWER THE QUESTION OR PERFORM A TASK.
        """
        return Form_groq().llama3_70b(system_prompt, context)
       
    def responder(self, context: Context) -> str: 
        '''
        This agent is a final piece in the puzzle. He is supposed to summarize thoughts,
        analyze documents or just simply respond to a question.
        '''
        system_prompt = """you are a helpful assistant. you will be provided users quesion
        or request as well as your internal reflection reqarding users request. your task is
        to help the user using all of your abilities DO NOT THINK, ANSWER 
        """
        return Form_groq().llama3_70b(system_prompt, context)




