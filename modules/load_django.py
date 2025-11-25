import os
import sys
import django
from pathlib import Path


current_file_path = Path(__file__).resolve()
project_path = current_file_path.parent.parent
sys.path.append(str(project_path))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barreaulyon_project.settings")

django.setup()