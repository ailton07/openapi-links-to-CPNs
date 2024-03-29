import snakes.plugins

from openapi.openapi2cpn import OpenAPI2PetriNet
from utils.log_utils import LogUtils
from utils.draw_utils import DrawUtils
from utils.string_utils import StringUtils

snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import Substitution  # added here to mute warnings


class Replay:
    @staticmethod
    def replay_execution_on_log(openapi_path, logs_path):
        """
        Given an OpenAPI documentation openapi_path and executions logs associated, logs_path,
        associated to this API, execute the replay and create images of the status.

        Args:
            openapi_path (string): OpenAPI documentation path
            logs_json (_type_): Logs path
        """
        # Load OpenAPI document
        open_api_to_petri_parser = OpenAPI2PetriNet(openapi_path)
        petri_net = open_api_to_petri_parser.create_petri_net(open_api_to_petri_parser.get_documentation_title())
        draws = {}
        DrawUtils.draw(draws, '0-initial-state.png', petri_net)
        #draws['0-initial-state.png'] = petri_net.draw("0-initial-state.png")

        # Load logs
        logs_json = LogUtils.load_logs(logs_path)

        for line_number in range(len(logs_json)):
            log_line = logs_json[line_number]
            
            transition = open_api_to_petri_parser.get_transition_from_log_line(log_line)
            if transition == None:
                print(f'Line {StringUtils.format_line_number(line_number)} is not present in the model: {log_line.get("message")}')
                continue

            fire_object = open_api_to_petri_parser.create_binding_from_request_line(log_line)
            try:
                try:
                    # Testing
                    # petri_net.place()[0].tokens.items()[0] == fire_object.get('id')
                    transition.fire(Substitution(fire_object))
                except ValueError as exception:
                    fire_object = open_api_to_petri_parser.create_binding_from_request_line(log_line, True)
                    transition.fire(Substitution(fire_object))
            except Exception as exception:
                print(f'Fire error, Line {StringUtils.format_line_number(line_number)}: {log_line.get("message")}')
                print(f'{exception}')
                continue
            DrawUtils.draw(draws, f"line-{StringUtils.format_line_number(line_number)}-fire-line.png", petri_net)

        return draws
