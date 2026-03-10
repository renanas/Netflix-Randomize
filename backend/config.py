from dotenv import load_dotenv
import os

load_dotenv()

# The prefix used for all API routes. We allow configuring it through
# the API_PREFIX environment variable but FastAPI will raise an
# AssertionError if the prefix ends with a slash ("/"). The default
# used to be "/" which triggered that error when no variable was set.
#
# To avoid problems we normalize the value:
#   * strip any trailing slashes
#   * ensure the prefix starts with a slash (if not empty)
#   * treat a single "/" as equivalent to an empty prefix
#
_api_prefix = os.getenv("API_PREFIX", "").rstrip("/")
if _api_prefix and not _api_prefix.startswith("/"):
    _api_prefix = "/" + _api_prefix

API_PREFIX = _api_prefix
