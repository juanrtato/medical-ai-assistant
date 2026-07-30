from app.assistant.graph import assistant

assistant.chat(session_id="123", message="Tengo fiebre.")

response = assistant.chat(session_id="123", message="Desde ayer.")

print(response)
