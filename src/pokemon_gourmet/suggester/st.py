__all__ = []

import sys
from pathlib import Path

from streamlit.web import cli


def main():
    file_path = Path(__file__).parent / "gui.py"
    args = ["streamlit", "run", str(file_path)]
    sys.argv = args
    sys.exit(cli.main())


if __name__ == "__main__":
    main()
