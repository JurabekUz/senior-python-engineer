from contextlib import contextmanager

CONFIG = {
    "DEBUG": False,
    "DB_NAME": "prod_db"
}


@contextmanager
def override_config(DEBUG, DB_NAME):

	CONFIG["DEBUG"] = DEBUG
	CONFIG["DB_NAME"] = DB_NAME

	yield

	CONFIG["DEBUG"] = False
	CONFIG["DB_NAME"] = "prod_db"


with override_config(DEBUG=True, DB_NAME="test_db"):
    print(CONFIG["DEBUG"])  # True

print(CONFIG["DEBUG"])  # False