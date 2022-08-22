import snakes.plugins

from replay.coloured_token import ColouredToken, RequestResponseToken
from utils.constants import RESPONSE_BODY
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils

snakes.plugins.load("gv", "snakes.nets", "nets")
from prance import ResolvingParser
from nets import PetriNet, Place, Expression, Transition, Variable  # added here to mute warnings
from utils.openapi_utils import OpenAPIUtils


class OpenAPI2PetriNet:
    parser = ''
    petri_net = None
    default_documentation_title = 'OpenAPI Document'

    def __init__(self, openapi_path):
        self.parser = ResolvingParser(openapi_path)

    def create_petri_net(self, name):
        self.petri_net = PetriNet(name)
        petri_net = self.petri_net

        spec = self.parser.specification
        paths = spec.get('paths')

        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            # transition 1
            # creating basic structure
            # transition = self.create_transition_and_basic_places(petri_net, uri)

            # cheking the OperationObjects
            for operation_object_key, operation_object_value in path_value.items():
                requestBody = operation_object_value.get('requestBody')
                parameters = operation_object_value.get('parameters')
                for response_key, response_object_value in operation_object_value.get('responses').items():
                    transition = self.create_transition(uri, operation_object_key, response_key)

                    self.handle_request_body(transition, requestBody)
                    self.handle_parameters(transition, parameters)
        
        self.create_link_arcs()
        return petri_net


    def create_link_arcs(self):
        spec = self.parser.specification
        for path_key, path_value in spec.get('paths').items():
            uri = path_key
            # cheking the OperationObjects
            for operation_object_key, operation_object_value in path_value.items():
                for response_key_status_code, response_object_value in operation_object_value.get('responses').items():
                    transition_name = OpenAPIUtils.create_transition_name(operation_object_key, uri, response_key_status_code)
                    transition = OpenAPIUtils.get_transition_by_name(self.petri_net, transition_name)

                    links = OpenAPIUtils.extract_links_from_response(response_object_value)
                    for link in links:
                        for link_value in link.values():
                            # create arc to the following input
                            operation_id = link_value.get('operationId')
                            parameters_key_value = link_value.get('parameters')
                            if parameters_key_value:
                                ((parameter_id, parameter_value),) = parameters_key_value.items()
                                nex_transition_name = OpenAPIUtils.get_transition_by_operation_id(spec, operation_id)
                                input_place = OpenAPIUtils.get_place_by_name(
                                    self.petri_net, OpenAPIUtils.create_place_name_to_parameter(parameter_id, nex_transition_name))

                                if RESPONSE_BODY in parameter_value:
                                    expression_str = f"request.get_token_from_reponse_body('{parameter_value.replace(RESPONSE_BODY, '')}')"
                                    self.petri_net.add_output(input_place.name, transition.name, Expression(expression_str))
                                

    def handle_request_body(self, transition, requestBody):
        if (requestBody):
            content = requestBody.get('content')
            for contentKey, contentValue in content.items():
                if (contentValue.get('schema')):
                    schema = contentValue.get('schema')
                    # possible values of schema type https://yaml.org/spec/1.2-old/spec.html#id2803231
                    type = schema.get('type')
                    if (type == 'object'):
                        properties = schema.get('properties')
                        for property_key, property_value in properties.items():
                            property_name = property_key
                            self.create_place_and_connect_as_input(transition, property_name)

    def handle_parameters(self, transition, parameters):
        if (parameters):
            for parameter in parameters:
                self.create_place_and_connect_as_input(transition, parameter.get('name'))

    # this the response place
    def handle_responses_status_code(self, uri, transition, responses):
        if (responses):
            for responseKey, responseValue in responses.items():
                content = responseValue.get('content')
                if content:
                    for contentKey, contentValue in content.items():
                        content_type = contentKey
                        schema = contentValue.get('schema')
                        place = Place(f'Response-{uri}', [])
                        if OpenAPIUtils.get_place_by_name(self.petri_net, place.name) is None:
                            self.petri_net.add_place(place)
                            self.petri_net.add_output(place.name, transition.name, Expression("request.get_response()"))

    # def create_transition(self, uri, operation_object_key):
    #     # creating transition
    #     transition = Transition(OpenAPIUtils.create_transition_name(operation_object_key, uri))
    #     # conecting the transtion with the CPN
    #     self.petri_net.add_transition(transition)
    #     return transition

    def create_transition(self, uri, operation_object_key, status_code):
        # creating transition
        transition = Transition(OpenAPIUtils.create_transition_name(operation_object_key, uri, status_code))
        # conecting the transtion with the CPN
        self.petri_net.add_transition(transition)
        return transition

    def create_place_and_connect_as_input(self, transition, property_name):
        place = Place(OpenAPIUtils.create_place_name_to_parameter(property_name, transition.name), [])
        connected_place = OpenAPIUtils.get_place_by_name(self.petri_net, place.name)
        if connected_place == None:
            self.petri_net.add_place(place)
            self.petri_net.add_input(place.name, transition.name, Variable(property_name))
        else:
            self.petri_net.add_input(connected_place.name, transition.name, Variable(property_name))


    # CHECK TODO
    # TODO: is not working for url paramenters (path parameters)
    def fill_input_places(self, log_json):
        for transition in self.petri_net.transition():
            if StringUtils.compare_uri_with_model(transition.name,
                                                  LogUtils.extract_http_method_with_uri_low_case(log_json)):
                # given a transistiopen_api_to_petri_parser.fill_input_places(log_line)on, check if we have some input to set
                # setting tokens related to requestBody
                request_body_parameter_names = LogUtils.extract_request_body_names_from_log(log_json)
                path_parameter_dict = LogUtils.extract_path_parameter_from_log(log_json, transition.name)
                places = transition.input()
                if len(request_body_parameter_names) > 0:
                    for parameter_name in request_body_parameter_names:
                        for place in places:
                            # se o place for output de alguma transição, nao devemos colocar tokens
                            if OpenAPIUtils.place_is_output(self.petri_net, place[0]):
                                continue
                            if place[0].name == OpenAPIUtils.create_place_name_to_parameter(parameter_name,
                                                                                            transition.name):
                                place[0].add(ColouredToken(
                                    LogUtils.create_data_from_request_body_in_log(log_json, parameter_name)))
                                break;
                # setting tokens related to parameters
                elif len(path_parameter_dict) > 0:
                    for key, value in path_parameter_dict.items():
                        for place in places:
                            # se o place for output de alguma transição, nao devemos colocar tokens
                            if OpenAPIUtils.place_is_output(self.petri_net, place[0]):
                                continue
                            if place[0].name == OpenAPIUtils.create_place_name_to_parameter(key,
                                                                                            transition.name):
                                place[0].add(ColouredToken(
                                    LogUtils.create_data_custom_from_log(key, value, log_json)))
                                break;

    def get_parser(self):
        return self.parser

    
    
    def find_path_object_by_name(self, path_name):
        """ Given a path_name, por example, '/login', return the path objecy
        from OpenAPI specification

        Args:
            path_name (string): the name of the path object, in other words, the path, example: '/signup'

        Returns:
            json object: path objecy from OpenAPI specification
        """
        for path_object_key, path_object_value in self.parser.specification.get('paths').items():
            if path_object_key == path_name:
                return {path_object_key: path_object_value}
            else:
                # se o path_object nao foi encontrado pelo metodo anterior, e possivel que o path tenha um parametro
                if StringUtils.compare_uri_with_model(path_object_key, path_name):
                    return {path_object_key: path_object_value}


    # TODO: extract data from url    
    def create_binding_from_request_line(self, log_json_request_line):
        binding = {}
        url = LogUtils.extract_uri_from_log(log_json_request_line)
        status_code = LogUtils.extract_status_code_from_log(log_json_request_line)
        transition_name = OpenAPIUtils.create_transition_name(log_json_request_line.get('method'), url, status_code)
        transition = OpenAPIUtils.get_transition_by_name(self.petri_net, transition_name)
        
        if transition == None:
            return None

        for variable in transition.pre.values():
            variable_name = variable.name
            request_body = LogUtils.extract_request_body_from_log(log_json_request_line)
            # check only in the first level if the variable_name is present
            # TODO: check object sublevels, for example, if we are looking for 'email', 
            # the object can be request_body.attribute1.obj2.email
            variable_in_request_body = request_body.get(variable_name)
            if variable_in_request_body != None:
                binding[variable_name] = ColouredToken(
                    LogUtils.create_data_custom_from_log(
                        variable_name,
                        variable_in_request_body,
                        log_json_request_line
                        )
                    )
                continue
            else:
                # 1. check query parameter
                # TODO: implement this case
                # 2. check url value
                path_object = self.find_path_object_by_name(url)
                if path_object:
                    dict_in_url = StringUtils.extract_url_value_from_url(list(path_object.keys())[0], url)
                    coloured_token = ColouredToken(LogUtils.create_data_custom_from_log_with_dict(dict_in_url, log_json_request_line))
                    variable_name = list(dict_in_url.keys())[0]
                    binding[variable_name] = coloured_token
        
        request_line = RequestResponseToken(*LogUtils.create_request_response_from_log(log_json_request_line))
        binding['request'] = request_line
        return binding
        
    def get_transition_from_log_line(self, log_line):
        """ Returns the transition associated to a given log line

        Args:
            log_line (_type_): the log line in json format.
            ex: {"timestamp":"2022-02-08T16:51:17.653Z","ip":"::ffff:127.0.0.1","message":"GET /accounts/6 200 84ms","method":"GET","uri":"/accounts/6","requestBody":{},"responseBody":{"status":"success","data":{"id":6,"coupon":null,"createdAt":"2022-02-08T16:51:17.548Z","updatedAt":"2022-02-08T16:51:17.548Z","UserId":21,"Products":[]}},"statusCode":200}

        Returns:
            _type_: find the transition associated to that log line
        """
        transitions = self.petri_net.transition()
        url = LogUtils.extract_uri_from_log(log_line)
        method = LogUtils.extract_method_from_log(log_line)
        status_code = LogUtils.extract_status_code_from_log(log_line)

        for transition in transitions:
            calculated_transition_name = OpenAPIUtils.create_transition_name(method, url, status_code)
            if StringUtils.compare_uri_with_model(transition.name, calculated_transition_name):
                return transition
        return None

    def get_documentation_title(self):
        if self.parser.specification.get('info').get('title'):
            return self.parser.specification.get('info').get('title')
        else:
            return self.default_documentation_title