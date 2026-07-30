from app.rag.retriever import retrieve_protocol

query = """
Paciente con fiebre de 39 grados desde hace dos días y dolor de garganta.
"""

context = retrieve_protocol(query)

print(context)
