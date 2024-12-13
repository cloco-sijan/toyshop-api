"""
Utility to discover models for database migrations

Import and invoke this function after initializing alembic,
in env.py file
"""

import importlib
import pkgutil


def import_submodules(package_name):
    """Import all submodules of a given package"""

    package = importlib.import_module(package_name)
    results = {}

    for _, name, _ in pkgutil.walk_packages(package.__path__):
        full_name = f"{package_name}.{name}"

        try:
            results[full_name] = importlib.import_module(full_name)
        except ImportError:
            print(f"Could not import {full_name}")

    return results
