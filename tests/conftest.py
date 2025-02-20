import os
import pytest

@pytest.fixture(scope="session", autouse= True)
def set_env_variable():
    os.environ["BASE_URL"]="https://www.kurly.com/main"
    os.environ["CI"] = "true"
    os.environ["USER_DATA_DIR"] = os.path.join(os.getcwd(),"selenium_profile")
    yield


