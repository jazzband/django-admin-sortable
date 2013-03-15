#!/usr/bin/env python
import os
import sys

# Adds the adminsortable package from the cloned repository instead of site_packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
