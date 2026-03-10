import sys
import os
import importlib

# put project root on path so `backend` package can be resolved during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backend.config as config


def reload_config():
    importlib.reload(config)
    return config.API_PREFIX


def test_default_prefix_empty(monkeypatch):
    """When no environment variable is defined we should get an empty prefix."""
    # remove any existing variable and prevent dotenv from reintroducing it
    monkeypatch.delenv("API_PREFIX", raising=False)
    # make sure dotenv.load_dotenv is a no-op while we reload config
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)

    assert reload_config() == ""


def test_trailing_slash_stripped(monkeypatch):
    """A value ending in '/' should be normalized by removing the slash."""
    monkeypatch.setenv("API_PREFIX", "/api/")
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    assert reload_config() == "/api"


def test_root_slash_becomes_empty(monkeypatch):
    """A lone '/' should be treated as if no prefix was provided."""
    monkeypatch.setenv("API_PREFIX", "/")
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    assert reload_config() == ""


def test_missing_leading_slash(monkeypatch):
    """If the variable doesn't start with '/', we add it automatically."""
    monkeypatch.setenv("API_PREFIX", "version1")
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    assert reload_config() == "/version1"
