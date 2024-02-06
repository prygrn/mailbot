import mailbot
import pytest

@pytest.fixture
def correct_arguments():
    return ["mailbot.py", ".env/oauth_token.json"]


def test_check_token_path():
    assert mailbot.check_token_path("/okdz!&1/$") == False
    assert mailbot.check_token_path("/usr/bin/cat") == True


def test_check_arguments(correct_arguments):
    assert mailbot.check_arguments([]) == False
    assert mailbot.check_arguments(["mailbot.py"]) == False
    assert mailbot.check_arguments(["mailbot.py", "/invalid/path"]) == False
    assert mailbot.check_arguments(["mailbot.py", "argument1", "argument2", "argument3"]) == False
    assert mailbot.check_arguments(correct_arguments) == True
