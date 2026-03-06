"""
AI prompt + response logger — stores every Gemini call in ai_logs table.
"""
import time
from app.database import get_connection, new_id, now_iso


def log_ai_call(module: str, prompt: str, response: str, latency_ms: int) -> None:
    """Persist a single AI call to the ai_logs table."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO ai_logs (id, module, prompt, response, latency_ms, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (new_id(), module, prompt, response, latency_ms, now_iso()),
        )
        conn.commit()
    finally:
        conn.close()


class AICallTimer:
    """Context manager that measures latency and auto-logs the AI call."""

    def __init__(self, module: str, prompt: str):
        self.module = module
        self.prompt = prompt
        self._start: float = 0.0
        self.response: str = ""

    def __enter__(self):
        self._start = time.monotonic()
        return self

    def __exit__(self, *_):
        latency_ms = int((time.monotonic() - self._start) * 1000)
        log_ai_call(self.module, self.prompt, self.response, latency_ms)
