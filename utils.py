import os


def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_log_file(filename):
    base = os.path.join(os.getcwd(), "logs")
    full_path = os.path.join(base, filename)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
