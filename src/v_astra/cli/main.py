import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vastra",
        description="V-Astra Token Optimizer",
    )
    parser.add_argument("--version", action="version", version="0.1.0a1")
    parser.parse_args()


if __name__ == "__main__":
    main()
