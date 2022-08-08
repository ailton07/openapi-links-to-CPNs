import snakes.plugins

from coloured_token import ColouredToken, RequestResponseToken
from utils.log_utils import LogUtils

snakes.plugins.load("gv", "snakes.nets", "nets")
import json
from openapi.openapi2cpn import OpenAPI2PetriNet
from nets import Substitution  # added here to mute warnings

# OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml'
# LOGS_PATH = 'logs/combined_bola_example.json'
#TODO: testar com Structural_Problem_Based_on_BOLA_Example_02
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml', 'logs/combined_example_structural_problem.json'
OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml', 'logs/combined_example_structural_problem.json'

def replay_execution_on_log(openapi_path, logs_path):
    """

    Args:
        openapi_path (_type_): _description_
        logs_json (_type_): _description_
    """
    # Load OpenAPI document
    open_api_to_petri_parser = OpenAPI2PetriNet(openapi_path)
    petri_net = open_api_to_petri_parser.create_petri_net(open_api_to_petri_parser.get_documentation_title())
    petri_net.draw("0-initial-state.png")

    # Load logs
    logs_json = LogUtils.load_logs(logs_path)
    
    for line_number in range(len(logs_json)):
        log_line = logs_json[line_number]
        
        transition = open_api_to_petri_parser.get_transition_from_log_line(log_line)
        if transition == None:
            print(f'Line {line_number} is not present in the model')
            continue

        open_api_to_petri_parser.fill_input_places(log_line)
        petri_net.draw(f"1-input-places-line-{line_number}.png")

        fire_object = open_api_to_petri_parser.create_binding_from_request_line(log_line)
        transition.fire(Substitution(fire_object))
        petri_net.draw(f"2-fire-line-{line_number}.png")


def main():
    replay_execution_on_log(OPENAPI_PATH, LOGS_PATH)
    return None

# def main():
#     open_api_to_petri_parser = OpenAPI2PetriNet(OPENAPI_PATH)
#     petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
#     transitions = petri_net.transition()
#     petri_net.draw("value-0.png")

#     log_line = logs_json[1]
#     open_api_to_petri_parser.fill_input_places(log_line)
#     petri_net.draw("value-0.png")

#     fire_object = open_api_to_petri_parser.create_binding_from_request_line(log_line)
#     transition = open_api_to_petri_parser.get_transition_from_log_line(log_line)
#     transition.fire(Substitution(fire_object))
#     petri_net.draw("value-0.png")

#     log_line = logs_json[3]
#     open_api_to_petri_parser.fill_input_places(log_line)
#     petri_net.draw("value-0.png")

#     fire_object = open_api_to_petri_parser.create_binding_from_request_line(log_line)
#     transition = open_api_to_petri_parser.get_transition_from_log_line(log_line)
#     transition.fire(Substitution(fire_object))
#     petri_net.draw("value-0.png")
#     petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()
