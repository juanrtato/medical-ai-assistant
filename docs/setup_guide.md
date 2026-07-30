# Guía de Instalación, Configuración y Ejecución

Esta guía detalla los pasos para poner en marcha el proyecto **Emermédica AI Assistant** en un entorno local o de producción.

---

## 1. Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu sistema:
- **Python**: Versión 3.10 o superior (`python --version`).
- **Git**: Para clonar el repositorio.
- **OpenAI API Key**: Una clave de API activa de OpenAI para los modelos LLM y Embeddings (`gpt-4o-mini` y `text-embedding-ada-002` / `text-embedding-3-small`).
- **Docker y Docker Compose** *(Opcional)*: Para ejecución en contenedores aislados.

---

## 2. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:

```bash
cp .env.example .env
```

Configura las siguientes variables en `.env`:

```env
PORT=8000
HOST=0.0.0.0
ENV=development
OPENAI_API_KEY=tu_api_key_de_openai_aqui
MODEL=gpt-4o-mini
TEMPERATURE=0.2
```

---

## 3. Opción A: Ejecución Rápida con Docker (Recomendado)

La forma más sencilla de ejecutar la aplicación completa (Backend + Frontend):

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd emermedica-ai-assistant

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu OPENAI_API_KEY

# 3. Levantar los servicios con Docker Compose
docker-compose up --build
```

Una vez levantado:
- **Frontend (Streamlit)**: [http://localhost:8501](http://localhost:8501)
- **Backend (FastAPI)**: [http://localhost:8000](http://localhost:8000)
- **Documentación Swagger API**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 4. Opción B: Ejecución Manual Local (Sin Docker)

### Paso 1: Configurar el Entorno Virtual de Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activar en Linux / macOS:
source venv/bin/activate

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### Paso 2: Indexación de los Protocolos Médicos en ChromaDB

El sistema cuenta con un mecanismo de **Auto-Indexación al Iniciar**:
- **En Docker**: Al ejecutar `docker-compose up`, la aplicación backend (FastAPI) detecta si la base `ChromaDB` existe. Si no existe o está vacía, lee automáticamente todos los archivos markdown en `backend/app/knowledge/protocols/` y los indexa sin intervención manual.
- **Indexación Manual (Opcional)**: Si deseas forzar la regeneración de la base de datos vectorial localmente, puedes ejecutar:

```bash
python backend/index_protocols.py
```

### Paso 3: Iniciar el Backend (FastAPI)

```bash
cd backend
python main.py
```
El servidor backend se iniciará en `http://localhost:8000`.

### Paso 4: Iniciar el Frontend (Streamlit)

En una nueva consola con el entorno virtual activado:

```bash
cd frontend
streamlit run app.py
```
La interfaz web se abrirá automáticamente en `http://localhost:8501`.

---

## 5. Ejecución de Pruebas Automáticas

Puedes validar el funcionamiento del agente, el RAG y los nodos de triage ejecutando los scripts de prueba:

```bash
# Probar recuperación RAG
python backend/test_rag.py

# Probar agente conversacional
python backend/test_assistant.py

# Probar clasificación de Triage
python backend/test_triage.py
```

---

## 6. Solución de Problemas Frecuentes

| Problema | Causa Posible | Solución |
|---|---|---|
| **HTTP 500 Server Error** | `OPENAI_API_KEY` inválida o no configurada. | Revisa tu `.env` y confirma que la API Key de OpenAI sea válida. |
| **Error en RAG Retriever** | La base ChromaDB no ha sido indexada. | Ejecuta `python backend/index_protocols.py`. |
| **Puerto 8000 / 8501 ocupado** | Otro proceso está usando el puerto. | Cambia los puertos en `docker-compose.yml` o en `.env`. |
