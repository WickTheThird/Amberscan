from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


STATICFILES_DIRS = [
    BASE_DIR / 'frontend',
]
