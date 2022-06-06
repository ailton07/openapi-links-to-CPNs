from utils.string_utils import StringUtils


class OpenAPIUtils:

    @staticmethod
    def create_transition_name(operation_object_key, uri):
        return str.lower(f"{operation_object_key}-{uri}")

    @staticmethod
    def create_place_name_to_parameter(parameter_name, transition_name):
        return str.lower(f"{parameter_name} {transition_name}")

    @staticmethod
    def get_place_by_name(petri_net, name):
        response = [x for x in petri_net.place() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in petri_net.place() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None

    @staticmethod
    def place_is_output(petri_net, place):
        transitions = petri_net.transition()
        for transition in transitions:
            for output in transition.output():
                if output[0].name == place.name:
                    return True
        return False

    @staticmethod
    def extract_request_body_from_log(log_json):
        return [*log_json.get('requestBody').keys()]  # convert dict to array

    @staticmethod
    def extract_query_parameter_from_log(log_json, transition):
        result = {}
        if OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri')) == transition.name:
            return result
        transition_uri_splited = transition.name.split('-')[1].split('/')
        log_uri_splited = log_json.get('uri').split('/')

        if (len(transition_uri_splited) == len(log_uri_splited)):
            for i in range(len(transition_uri_splited)):
                if (transition_uri_splited[i] != log_uri_splited[i]):
                    if ('{' in transition_uri_splited[i]):
                        key = transition_uri_splited[i].replace("{", "").replace("}", "")
                        value = log_uri_splited[i]
                        result[key] = value
        else:
            return result
        return result
