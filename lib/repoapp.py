import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="research-repo",
        description="CLI tool to manage your research repository"
    )

    parser.add_argument("command", choices=["init", "add", "list"], help="Command to run")
    parser.add_argument("--title", "-t", help="Title of the research paper")

    args = parser.parse_args()

    if args.command == "init":
        print("Initializing research repo...")
    elif args.command == "add":
        print(f"Adding new research paper: {args.title}")
    elif args.command == "list":
        print("Listing all research papers...")
