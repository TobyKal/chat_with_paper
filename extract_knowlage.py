import os
import ast
from typing import Union
from PyPDF2 import PdfReader
import time
from llms.llm_interfaces import form_groq
from llms.context import context



def handle_pdf(file_path: str) -> Union[str, None]:
    try:
        pdf = PdfReader(file_path)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    

def create_substings(text: str) -> None:
    start = 0
    end = 3000

    while start < len(text):
        if end < len(text):
            while end < len(text) and text[end] not in {".", "!", "?"}:
                end += 1
        else:
            end = len(text)

        substring = text[start:end+1]

        try:
            extract_bits_of_knowlage(substring)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 1 minute...")
            time.sleep(60)
            try:
                extract_bits_of_knowlage(substring)
            except Exception as e:
                print(f"process_substing failed ''{e}'' ending that buissness fix that stuff choom!")
                exit()
        start = end + 1
        end = start + 3000



def extract_bits_of_knowlage(substing: str) -> None:
    system_prompt = """You are an advanced algorithm that
is responds with a bits of knowlage extracted form the supplied in a form of python list of stings.
DO NOT RESPOND WITH ANYTHING ELSE YOUR LIFE DEPENDS ON IT"""

    log = context()
    log.add_user_message(substing)
    model = form_groq().llama3_70b
    
    bits_of_knowlage = None
    for i in range(10):
        try:
            bits_of_knowlage = model(system_prompt, log.to_list())
            bits_of_knowlage = ast.literal_eval(bits_of_knowlage)
            break
        except Exception as e:
            print(f"An error occurred on attempt {i+1}: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)
    if bits_of_knowlage is None:
        print("All attempts failed.")
        raise Exception("All attempts failed.")
    else:
        print(bits_of_knowlage) #for testing only
    # here i need to contuinue further processing of hte information 
    # main idas are instead of making a bunch of small bit of knowlage 
    # make one big BYTE of knowlage or mabe even a MEGABYTE of kwlage but idk
    # the problems i see are as follows the bits of konwlage will be too diluted
    # and llm will not know what bit of knowlage belogs where but that requires testing 
    # i would assume that the training gave them enough information to understand 
    # the context of a given bit of knowlage and nad give a good answer but idk choom
    # its a future Toby's problem :D




def process_documents(documents_folder: str = r"C:\Users\Tobiasz\Documents\GitHub\chat_with_paper\files\documents") -> None:
    for filename in os.listdir(documents_folder):
        print(f"Processing file: {filename}")
        file_path = os.path.join(documents_folder, filename)

        if filename.endswith('.pdf'):
            text = handle_pdf(file_path)

        if text is not None:
            create_substings(text) 
        print(f"\n Document: {filename} has been processed!\n Time to remove that document\n")
        #os.remove(file_path) for testing 
    print('All of the files has beenprocessed')


if __name__ == "__main__":
    process_documents()