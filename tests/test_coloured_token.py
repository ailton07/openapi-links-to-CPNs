
import json

import pytest
from coloured_token import ColouredToken, RequestResponseToken
from utils.log_utils import LogUtils


@pytest.fixture
def get_logs(logs_name):
    LOGS_PATH = logs_name
    logs_file = open(LOGS_PATH)
    logs_json = json.load(logs_file)
    logs_file.close()
    return logs_json

@pytest.mark.parametrize("logs_name, line, expected_result", [
    # test with two parts item (authentication.umail)
    ("logs/combined_example_structural_problem.json", 1, 
     {'authentication.umail':'email@email.com'}),
    # test with one part item (status)
     ("logs/combined_example_structural_problem.json", 3, 
     {'status':'success'})
])
def test_get_from_reponse_body(logs_name, line, expected_result, get_logs):
    log_line = get_logs[line]
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    for key_value, expected_value in expected_result.items():
        value = request_line.get_from_reponse_body(key_value)
        assert value is not None 
        assert value == expected_value


@pytest.mark.parametrize("logs_name, line, expected_result", [
    # test with two parts item (authentication.umail)
    ("logs/combined_example_structural_problem.json", 1, 
     {'authentication.umail':'email@email.com'}),
    # test with one part item (status)
     ("logs/combined_example_structural_problem.json", 3, 
     {'status':'success'})
])
def test_get_key_value_from_response_body(logs_name, line, expected_result, get_logs):
    log_line = get_logs[line]
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    for key_value, expected_value in expected_result.items():
        result = request_line.get_key_value_from_response_body(key_value)
        assert result is not None 
        assert result == {str.split(key_value, '.')[-1]: expected_value}


@pytest.mark.parametrize("logs_name, line, expected_result", [
    # test with two parts item (authentication.umail)
    ("logs/combined_example_structural_problem.json", 1, 
     {'authentication.umail':{"umail":"email@email.com","user_id":"::ffff:127.0.0.1"}}),
    # test with one part item (status)
     ("logs/combined_example_structural_problem.json", 3, 
     {'status':{"status":"success","user_id":"::ffff:127.0.0.1"}})
])
def test_get_token_from_reponse_body(logs_name, line, expected_result, get_logs):
    log_line = get_logs[line]
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    for key_value, expected_value in expected_result.items():
        result = request_line.get_token_from_reponse_body(key_value)
        assert result is not None 
        assert result == ColouredToken(expected_value)