#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py migrate --noinput
# Seed only when DB is empty (first deploy)
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from records.models import NormalizedRecord
if NormalizedRecord.objects.count() == 0:
    import subprocess
    subprocess.check_call(['python', 'scripts/seed.py'])
"
