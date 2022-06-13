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
    def get_transition_by_name(petri_net, name):
        response = [x for x in petri_net.transition() if x.name == name]
        if (response and len(response) > 0):
            return response[0]
        else:
            # se o place nao foi encontrado pelo metodo anterior, e possivel que o path tenha um
            # parametro
            response = [x for x in petri_net.transition() if StringUtils.compare_uri_with_model(x.name, name)]
            if (response and len(response) > 0):
                return response[0]
        return None


    @staticmethod
    def extract_links_from_responses(responses):
        links_set = []
        if (responses):
            for responseKey, responseValue in responses.items():
                links = responseValue.get('links')
                if links:
                    links_set.append(links)
        return links_set


    def get_transition_by_operation_id(spec, operation_id):
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            for operation_object_key, operation_object_value in path_value.items():
                uri = OpenAPIUtils.create_transition_name(operation_object_key, uri)
                operationId = operation_object_value.get('operationId')
                if operationId == operation_id:
                    return uri