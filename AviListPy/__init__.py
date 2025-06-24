# -*- coding: utf-8 -*-
"""
AviListPy
==============================================================================
Python implementation of the 2025 AviList Global Avian Checklist.

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

Citations:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025.
https://doi.org/10.2173/avilist.v2025
"""
from pathlib import Path

# Package metadata
__author__ = 'Thomas Lee'
__email__ = 'tl165@rice.edu'
__license__ = 'CC0-1.0'

def _get_version():
    """Read version from pyproject.toml file."""
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        try:
            import tomli as tomllib  # Fallback for older Python
        except ImportError:
            # Final fallback - try to parse manually or return default
            return "unknown"

    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
        return pyproject_data["project"]["version"]
    except (FileNotFoundError, KeyError, Exception):
        # Fallback version if reading fails
        return "unknown"

__version__ = _get_version()

from AviListPy.data.avilistdatabase import AviListDataBase
from AviListPy.taxonomy.species import Species
from AviListPy.taxonomy.genus import Genus
from AviListPy.taxonomy.family import Family
from AviListPy.taxonomy.order import Order
from AviListPy.taxonomy.subspecies import Subspecies

__all__ = ['AviListDataBase', 'Order', 'Family', 'Genus', 'Species', 'Subspecies']
