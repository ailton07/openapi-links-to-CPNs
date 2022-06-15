import snakes.plugins

from coloured_token import ColouredToken, RequestResponseToken
from utils.log_utils import LogUtils

snakes.plugins.load("gv", "snakes.nets", "nets")
import json
from openapi.openapi2cpn import OpenAPI2PetriNet
from nets import Substitution  # added here to mute warnings

OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml'
LOGS_PATH = 'logs/combined_bola_example.json'
LOGS_PATH = 'logs/combined_example_structural_problem.json'
logs_file = open(LOGS_PATH)
logs_json = json.load(logs_file)
logs_file.close()


def main():
    open_api_to_petri_parser = OpenAPI2PetriNet(OPENAPI_PATH)
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    petri_net.draw("value-0.png")

    log_line = logs_json[1]
    open_api_to_petri_parser.fill_input_places(log_line)
    petri_net.draw("value-0.png")

    # fire 
    request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_line))
    email = ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'email'))
    password = ColouredToken(LogUtils.create_data_from_request_body_in_log(log_line, 'password'))
    authentication = ColouredToken(LogUtils.create_response_data_from_log(log_line, 'authentication'))

    transitions[0].fire(Substitution(request=request_line, email=email, password=password, authentication=authentication))
    petri_net.draw("value-0.png")

    log_line = logs_json[3]
    open_api_to_petri_parser.fill_input_places(log_line)
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
