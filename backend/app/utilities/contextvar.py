import contextvars

contextvar_locale = contextvars.ContextVar("locale", default="en")
contextvar_session_user_id = contextvars.ContextVar("session_user_id", default=0)
contextvar_correlation_id = contextvars.ContextVar("correlation_id", default=None)
contextvar_endpoint = contextvars.ContextVar("endpoint", default=None)
