from app.llm.client import llm

response = llm.invoke("Hola, ¿quién eres?")

print(response.content)
