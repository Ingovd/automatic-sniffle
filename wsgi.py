import os

import argparse

from jigs import create_app


CLI_WELCOME = "Microservice to gather Jigsaw Island usage statistics."
CLI_PROJECT_HELP = "The GCP project ID associated with the datastore."
CLI_PATH_HELP = "Path to instance folder with settings."

def main():
    parser = argparse.ArgumentParser(description=CLI_WELCOME)
    parser.add_argument('--project', help=CLI_PROJECT_HELP)
    parser.add_argument('-p', '--path', help=CLI_PATH_HELP, nargs='?')

    args = parser.parse_args()
    path = setup_instance_path(args.path)

    config = {'INSTANCE_PATH': path, "PROJECT": args.project}

    app = create_app(config)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


def setup_instance_path(path):
    if path is None:
        return None
    if os.path.isdir(path):
        return path
    abs_path = os.getcwd() + path
    if os.path.isdir(abs_path):
        return abs_path
    raise OSError(f"Neither {path} nor {abs_path} exists.")


if __name__ == "__main__":
    main()
