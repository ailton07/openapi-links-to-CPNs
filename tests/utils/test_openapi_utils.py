import pytest

from openapi.openapi2cpn import OpenAPI2PetriNet
from utils.openapi_utils import OpenAPIUtils


@pytest.fixture
def get_juice_shop_petri_net(filename):
    # open_api_to_petri_parser = OpenAPI2PetriNet(f'../examples/{filename}')
    open_api_to_petri_parser = OpenAPI2PetriNet(f'tests/examples/{filename}')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    return open_api_to_petri_parser, petri_net


@pytest.mark.parametrize("filename,expected_names", [
    ("Structural_Problem_Based_on_BOLA_Example_02.yaml",
     ['id get-/accounts/{id}']),
    ("Structural_Problem_Based_on_BOLA_Example.yaml",
     ['id get-/accounts/{id}']),
    ("JuiceShop.yaml",
     ['bid get-/rest/basket/{bid}']
     ),
])
def test_get_place_by_name(filename, expected_names, get_juice_shop_petri_net):
    # given the OpenApi specification and the corresponding petri net
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net

    # when call get_place_by_name
    for expected_name in expected_names:
        place = OpenAPIUtils.get_place_by_name(petri_net, expected_name)

        # we obtain places with names in expected_names list
        assert place is not None
        assert place.name == expected_name


@pytest.mark.parametrize("filename,expected_result", [
    ("Structural_Problem_Based_on_BOLA_Example_02.yaml",
     2),
    ("Structural_Problem_Based_on_BOLA_Example.yaml",
     2),
    ("JuiceShop.yaml",
     1),
])
def test_extract_links_from_paths_object(filename, expected_result, get_juice_shop_petri_net):
    # given the OpenApi specification and the corresponding petri net
    open_api_to_petri_parser, petri_net = get_juice_shop_petri_net
    # when call get_place_by_name
    links = OpenAPIUtils.extract_links_from_paths_object(open_api_to_petri_parser.parser)
    # we obtain places with names in expected_names list
    assert len(links) == expected_result
