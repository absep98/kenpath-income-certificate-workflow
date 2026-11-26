"""Test setup: point the app at a throwaway database BEFORE any app module is imported,
so API tests never touch the real demo database."""
import os
import tempfile

_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_dir}/test.db"
os.environ["DEMO_SEED"] = "0"
