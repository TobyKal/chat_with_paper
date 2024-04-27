import os
from typing import Union
from PyPDF2 import PdfReader

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