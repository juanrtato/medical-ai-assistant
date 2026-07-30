from app.assistant.graph import assistant

session_id = "test-triage"

# Simula una conversación
assistant.chat(session_id, "Tengo dolor fuerte en el pecho desde hace una hora.")
assistant.chat(session_id, "También me cuesta respirar.")

# Ejecuta el triage
result = assistant.triage(session_id)

print(result)
