"""
Routes package initialization
"""
# This file can be empty or import routers for easier access
from . import auth, analysis, health

__all__ = ["auth", "analysis", "health"]