from utils.string_utils import StringUtils


class OpenAPIUtils:

    # @staticmethod
    # def create_transition_name(operation_object_key, uri):
    #     return str.lower(f"{operation_object_key}-{uri}")

    @staticmethod
    def create_transition_name(operation_object_key, uri, status_code):
        return str.lower(f"{operation_object_key}-{uri}-{status_code}")

    @staticmethod
    def remove_code_from_transition_name(transition_name):
        transition_name_splited = transition_name.split("-")
        return str.lower(f"{transition_name_splited[0]}-{transition_name_splited[1]}")

    @staticmethod
    def create_place_name_to_parameter(parameter_name, transition_name):
        return str.lower(f"{parameter_name} {OpenAPIUtils.remove_code_from_transition_name(transition_name)}")

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
        """Receives a Responses Object, in other words, a object where the keys are status codes
        and the values are Response Objects. Returns a list of links

        Args:
            responses (list): List of responses. 
            Ex: {'200': {'description': 'search results match...g criteria', 'content': {...}, 'links': {...}}, '404': {'description': 'user not found', 'content': {...}, 'links': {...}}}

        Returns:
            list: A list of links. Ex: [{'getBasketById': {...}}, {'goToSignup': {...}}]
        """
        links_set = []
        if (responses):
            for responseKey, responseValue in responses.items():
                links = responseValue.get('links')
                if links:
                    links_set.append(links)
        return links_set


    @staticmethod
    def extract_links_from_paths_object(parser):
        """ Returns all the links of and OpenAPI Specification. 
        Receives a OpenAPI parser, in other words, a object where the keys are paths
        and the values are Path Item Object. Returns a list of links

        Args:
            responses (list): List of responses. 
            Ex: {'200': {'description': 'search results match...g criteria', 'content': {...}, 'links': {...}}, '404': {'description': 'user not found', 'content': {...}, 'links': {...}}}

        Returns:
            list: A list of links. Ex: [{'getBasketById': {...}}, {'goToSignup': {...}}]
        """
        links_set = []
        if (parser):
            for path_key, path_item_object_value in parser.specification.get('paths').items():
                for operation_object_key, operation_object_value in path_item_object_value.items():
                    responses_object = operation_object_value.get('responses')
                    for status_code_key, response_object_value in responses_object.items():
                        links = response_object_value.get('links')
                        if links:
                            links_set.append(links)
        return links_set


    @staticmethod
    def extract_links_from_response(response):
        """Receives a Response Object and returns a list of links

        Args:
            response (Response Object): A Response Object.
            Ex: {'description': 'search results match...g criteria', 'content': {...}, 'links': {...}}

        Returns:
            list: A list of links. Ex: [{'getBasketById': {...}}, {'goToSignup': {...}}]
        """
        links_set = []
        if (response):
            links = response.get('links')
            if links:
                links_set.append(links)
        return links_set
    
    
    @staticmethod
    def get_status_code_from_transition(transition):
        """Receives a Transition object and extracts the Status Code in its name.
        Ex: Given the transiton get-/rest/basket/{bid}-200, returns 200.

        Args:
            transition (Transition): A transition object

        Returns:
            String: The Status Code in the transition name.
        """
        transition_name = transition.name
        transition_splited = transition_name.split('-')
        last_element = transition_splited[-1]
        return last_element


    def get_transition_by_operation_id(spec, operation_id):
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            for operation_object_key, operation_object_value in path_value.items():
                for response_key, response_object_value in operation_object_value.get('responses').items():
                    uri = OpenAPIUtils.create_transition_name(operation_object_key, uri, response_key)
                    operationId = operation_object_value.get('operationId')
                    if operationId == operation_id:
                        return uri
