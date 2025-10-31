from . import mk_app
import waitress
import os

if __name__ == "__main__":
    waitress.serve(
        mk_app(),
        port=int(os.environ.get("LISA_HTTP_PORT", "80")),
        host=os.environ.get("LISA_HTTP_HOST", "0.0.0.0"),
    )
