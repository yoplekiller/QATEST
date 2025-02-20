import os

import pytest


@pytest.fixture(scope="session")
def api_url():
    return os.getenv("API_BASE_URL", "http://localhost:5000")
