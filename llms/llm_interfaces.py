import anthropic
import os
from dotenv import load_dotenv
from groq import Groq

class from_antropic:
    def __init__(self) -> None:
        load_dotenv()
        self.key = os.getenv("ANTROPIC_API")


    def haiku(self, system_prompt: str, context: str):
        client = anthropic.Anthropic(
            api_key= self.key
        )
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=context
        )
        return message.content

    def sonnet(self, system_prompt: str, context: list[dict]):
        client = anthropic.Anthropic(
            api_key= self.key
        )
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=context
        )
        return message.content
    
    def opus(self, system_prompt: str, context: str):
        client = anthropic.Anthropic(
            api_key= self.key
        )
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=0.3,
            system=system_prompt,
            messages=context
        )
        return message.content
    

class form_groq:
    def __init__(self) -> None:
        load_dotenv()
        self.key = os.getenv('GROQ')

    def llama3_8b(self, system_prompt: str, context: list[dict]):
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        client = Groq(api_key=self.key)

        response = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=context, 
            max_tokens=8192
        )
        return response.choices[0].message.content

    def llama3_70b(self, system_prompt: str, context: list[dict]):
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        client = Groq(api_key=self.key)

        response = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=context, 
            max_tokens=8192
        )
        return response.choices[0].message.content
    
    def llama2_70b(self, system_prompt: str, context: list[dict]):
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        client = Groq(api_key=self.key)

        response = client.chat.completions.create(
            model='llama2-70b-4096',
            messages=context, 
            max_tokens=4096
        )
        return response.choices[0].message.content
    
    def gemma_7B(self, system_prompt: str, context: list[dict]):
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        client = Groq(api_key=self.key)

        response = client.chat.completions.create(
            model='gemma-7b-it',
            messages=context, 
            max_tokens=8192
        )
        return response.choices[0].message.content
    
    def mixtral_8x7B(self, system_prompt: str, context: list[dict]):
        template = {"role": "system", "content": f"{system_prompt}"}
        context.insert(0, template)
        
        client = Groq(api_key=self.key)

        response = client.chat.completions.create(
            model='mixtral-8x7b-32768',
            messages=context, 
            max_tokens=32768
        )
        return response.choices[0].message.content