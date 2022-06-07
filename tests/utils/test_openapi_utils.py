import pytest

from openapi.openapi2cpn import OpenAPI2PetriNet
from utils.openapi_utils import OpenAPIUtils


@pytest.fixture
def get_juice_shop_petri_net(filename):
    # open_api_to_petri_parser = OpenAPI2PetriNet('../examples/Structural_Problem_Based_on_BOLA_Example_02.yaml')
    open_api_to_petri_parser = OpenAPI2PetriNet(f'../examples/{filename}')
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    return open_api_to_petri_parser, petri_net


@pytest.mark.parametrize("filename,expected_names", [
    ("Structural_Problem_Based_on_BOLA_Example_02.yaml",
     ['email post-/login', 'password post-/login', 'email post-/signup', 'password post-/signup']),
    ("Structural_Problem_Based_on_BOLA_Example.yaml",
     ['email post-/login', 'password post-/login', 'email post-/signup', 'password post-/signup',
      'id get-/accounts/{id}']),
    ("JuiceShop.yaml",
     ['email post-/rest/user/login', 'password post-/rest/user/login', 'bid get-/rest/basket/{bid}']
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
