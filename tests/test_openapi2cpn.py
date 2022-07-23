
import json
import pytest

from openapi.openapi2cpn import OpenAPI2PetriNet


@pytest.fixture
def get_juice_shop_petri_net(filename):
    # open_api_to_petri_parser = OpenAPI2PetriNet(f'../examples/{filename}')
    open_api_to_petri_parser = OpenAPI2PetriNet(f'tests/examples/{filename}')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    return open_api_to_petri_parser, petri_net


@pytest.fixture
def get_logs(logs_name):
    LOGS_PATH = logs_name
    logs_file = open(LOGS_PATH)
    logs_json = json.load(logs_file)
    logs_file.close()
    return logs_json


# TODO: COntinue here
@pytest.mark.parametrize("logs_name, line, filename, expected_result", [
    #
    ("logs/combined_example_structural_problem.json",
     1,
     "Structural_Problem_Based_on_BOLA_Example.yaml",
     {'email': 'email@email.com', 'password':'root123'}),
     ("logs/combined_example_structural_problem.json",
     3,
     "Structural_Problem_Based_on_BOLA_Example.yaml",
     {'id': '6'})
])
def test_create_binding_from_request_line(logs_name, line, filename, expected_result, get_logs, get_juice_shop_petri_net):
    assert True == True
    log_line = get_logs[line]
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net
    binding = open_api_to_petri_parser.create_binding_from_request_line(
        log_line)
    assert binding == expected_result


@pytest.mark.parametrize("filename, path_name, expected_result", [
    ("Structural_Problem_Based_on_BOLA_Example.yaml",
     "/login",
     True),
    ("Structural_Problem_Based_on_BOLA_Example.yaml",
     "/non-existent",
     False)
])
def test_find_path_object_by_name(filename, path_name, expected_result, get_juice_shop_petri_net):
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net
    response = open_api_to_petri_parser.find_path_object_by_name(path_name)
    assert (response != None) == expected_result
