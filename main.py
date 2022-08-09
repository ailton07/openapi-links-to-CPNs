from replay.replay import Replay

# OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml'
# LOGS_PATH = 'logs/combined_bola_example.json'
#TODO: testar com Structural_Problem_Based_on_BOLA_Example_02
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml', 'logs/combined_example_structural_problem.json'
OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml', 'logs/combined_example_structural_problem.json'


def main():
    #replay_execution_on_log(OPENAPI_PATH, LOGS_PATH)
    Replay.replay_execution_on_log(OPENAPI_PATH, LOGS_PATH)
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
