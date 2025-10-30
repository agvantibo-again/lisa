from . import create_app
from .users import User
import waitress


if __name__ == "__main__":
    waitress.serve(create_app())
