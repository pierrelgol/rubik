from src.main import main
import sys

if __name__ == "__main__":
    try:
        main(argc=len(sys.argv), argv=sys.argv)
    except Exception as e:
        print(f"{e}", file=sys.stderr, flush=True)
