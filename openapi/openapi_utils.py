from utils.string_utils import StringUtils

class OpenAPIUtils:

    @staticmethod
    def create_place_name_to_parameter(parameter_name, transition_name):
        return parameter_name + ' ' + transition_name

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