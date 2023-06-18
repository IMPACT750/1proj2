from .engine import Engine
from .view import AbstractView


def run():
    engine = Engine()

    engine.load_view(AbstractView.make_view("home"))
    engine.run()
