import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class LoggableMixin:
    """
    Mixin that adds logging capability to any class.
    Doesn't define __init__ or hold its own state — it just
    assumes the class it's mixed into has a `.name` attribute.
    """

    def log_action(self, action: str) -> None:
        logging.info(f"{self.__class__.__name__} '{self.name}' -> {action}")


class NotifiableMixin:
    """
    Mixin that adds a notify() capability.
    In real life this might send an email/SMS. For now, we simulate
    it with a print — but the interface is what matters: later we
    can swap the internals without touching any code that calls notify().
    """

    def notify(self, message: str) -> None:
        print(f"[NOTIFICATION to {self.name}] {message}")