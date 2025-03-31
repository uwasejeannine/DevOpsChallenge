"""
Run Django tests directly with coverage.
"""

import os
import sys

import django
from coverage import Coverage
from django.test.runner import DiscoverRunner

if __name__ == "__main__":
    # Set up Django
    os.environ["DJANGO_SETTINGS_MODULE"] = "fitness_booking.settings"
    django.setup()

    print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    # Set up coverage
    cov = Coverage(source=["booking"])
    cov.start()

    # Run tests
    test_runner = DiscoverRunner(verbosity=2)
    failures = test_runner.run_tests(["booking"])

    # Generate coverage report
    cov.stop()
    cov.save()
    cov.report()

    # Generate XML report for CI
    cov.xml_report(outfile="coverage.xml")

    # Exit with test status
    sys.exit(bool(failures))
