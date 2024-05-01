from llm_interfaces import Context, Form_groq, Agents

text= "A man dressed in all black in walking down a country lane. Suddenly, a large black car wiht no lights on comes around the corner and screeches to a halt. How did the car's driver konw he was there?"
system_prompt = "you are a helpfull asistant"
response = Form_groq().llama3_70b(system_prompt, text, Context())

print(response.to_list()[-1]["content"])




