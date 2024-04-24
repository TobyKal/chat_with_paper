class context:
    def __init__(self) -> None:
        self.messages = []

    def add_user_message(self, text: str) -> None:
        self.messages.append({"role": "user", "content": f"{text}"})

    def add_assistant_message(self, text: str) -> None:
        self.messages.append({"role": "assistant", "content": f"{text}"},)
    
    def delete_last_message(self) -> None:
        self.messages.pop(-1)

    def to_list(self):
        return self.messages