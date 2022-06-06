import snakes.plugins

from coloured_token import ColouredToken
from utils.log_utils import LogUtils
from utils.string_utils import StringUtils

snakes.plugins.load("gv", "snakes.nets", "nets")
from prance import ResolvingParser
from nets import PetriNet, Place, Expression, Transition, Variable  # added here to mute warnings
from utils.openapi_utils import OpenAPIUtils


class OpenAPI2PetriNet:
    parser = ''
    petri_net = None

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
                transition = self.create_transition(uri, operation_object_key)

                requestBody = operation_object_value.get('requestBody')
                self.handle_request_body(transition, requestBody)

                parameters = operation_object_value.get('parameters')
                self.handle_parameters(transition, parameters)

                responses = operation_object_value.get('responses')
                self.handle_responses(uri, transition, responses)
        self.petri_net = petri_net

        return petri_net

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

    def handle_responses(self, uri, transition, responses):
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

    def create_transition(self, uri, operation_object_key):
        # creating transition
        transition = Transition(OpenAPIUtils.create_transition_name(operation_object_key, uri))
        # conecting the transtion with the CPN
        self.petri_net.add_transition(transition)
        return transition

    def create_place_and_connect_as_input(self, transition, property_name):
        # TODO: verify if the place already exists
        place = Place(OpenAPIUtils.create_place_name_to_parameter(property_name, transition.name), [])
        self.petri_net.add_place(place)
        self.petri_net.add_input(place.name, transition.name, Variable(property_name))

    # TODO: is not working for url paramenters
    def fill_input_places(self, log_json):
        for transition in self.petri_net.transition():
            if StringUtils.compare_uri_with_model(transition.name,
                                                  LogUtils.extract_http_method_with_uri_low_case(log_json)):
                # given a transistiopen_api_to_petri_parser.fill_input_places(log_line)on, check if we have some input to set
                # setting tokens related to requestBody
                request_body_parameter_names = LogUtils.extract_request_body_from_log(log_json)
                query_parameter_dict = LogUtils.extract_query_parameter_from_log(log_json, transition)
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
                elif len(query_parameter_dict) > 0:
                    for key, value in query_parameter_dict.items():
                        for place in places:
                            # se o place for output de alguma transição, nao devemos colocar tokens
                            if OpenAPIUtils.place_is_output(self.petri_net, place[0]):
                                continue
                            if place[0].name == OpenAPIUtils.create_place_name_to_parameter(key,
                                                                                            transition.name):
                                place[0].add(ColouredToken(
                                    LogUtils.create_data_from_query_parameter_in_log(key, value, log_json)))
                                break;

    def get_parser(self):
        return self.parser
