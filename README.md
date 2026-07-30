# Emermédica AI Assistant

Realizado por: Juan Ricardo Albarracin Barbosa.

## Estructura del Proyecto

```text
emermedica-ai/
├── backend/            # API backend (FastAPI / Flask / Python)
├── frontend/           # Interfaz de usuario (Streamlit)
├── docs/               # Documentación, arquitectura y pruebas
├── docker-compose.yml  # Configuración para ejecución en contenedores
└── README.md
```

## Requisitos Previos

- Python 3.10+
- Docker & Docker Compose (opcional)

## Configuración y Ejecución

### Backend
```bash
cd backend
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
streamlit run app.py
```
