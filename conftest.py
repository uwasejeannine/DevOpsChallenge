"""
Configure Django for pytest.
This file must be placed in the root directory of your project.
"""

import os
import sys

import django
from django.conf import settings

# Add project to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django
os.environ["DJANGO_SETTINGS_MODULE"] = "fitness_booking.settings"
django.setup()

# Print debug information
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"Settings module exists: {hasattr(settings, 'INSTALLED_APPS')}")
