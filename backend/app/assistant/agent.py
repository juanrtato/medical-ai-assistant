from app.assistant.tools import retrieve_medical_protocol
from app.llm.client import llm

agent = llm.bind_tools([retrieve_medical_protocol])
