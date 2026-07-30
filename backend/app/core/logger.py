import logging
from collections import defaultdict
from contextvars import ContextVar

# ContextVar para asociar los logs con la sesión actual
current_session_id: ContextVar[str] = ContextVar("current_session_id", default="global")


class SessionLogHandler(logging.Handler):
    """Handler en memoria para capturar todos los logs del sistema por session_id."""

    def __init__(self):
        super().__init__()
        self.logs = defaultdict(list)

    def emit(self, record):
        try:
            msg = self.format(record)
            session_id = current_session_id.get("global")
            self.logs[session_id].append(msg)
        except Exception:
            self.handleError(record)

    def get_logs(self, session_id: str) -> list[str]:
        # Devuelve los logs específicos de la sesión y los globales
        logs = list(self.logs.get("global", []))
        if session_id != "global":
            logs.extend(self.logs.get(session_id, []))
        return logs

    def clear_logs(self, session_id: str):
        if session_id in self.logs:
            self.logs[session_id].clear()


session_log_handler = SessionLogHandler()
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
session_log_handler.setFormatter(formatter)

logger = logging.getLogger("emermedica")
logger.setLevel(logging.INFO)
logger.addHandler(session_log_handler)

# Configuración básica en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

