from utils.openapi_utils import OpenAPIUtils
from utils.string_utils import StringUtils


class LogUtils:
    @staticmethod
    def create_data_from_request_body_in_log(log_json, parameter):
        return {
            parameter: log_json.get('requestBody').get(parameter),
            'user_id': log_json.get('ip')
        }

    @staticmethod
    def create_data_custom_from_log(parameter, value, log_json):
        return {
            parameter: value,
            'user_id': log_json.get('ip')
        }

    @staticmethod
    def create_data_custom_from_log_with_dict(dict, log_json):
        dict['user_id'] =  log_json.get('ip')
        return dict

    @staticmethod
    def extract_http_method_with_uri_low_case(log_json):
        return OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri'))

    @staticmethod
    def extract_request_body_names_from_log(log_json):
        return [*log_json.get('requestBody').keys()]  # convert dict to array

    @staticmethod
    def extract_request_body_from_log(log_json):
        return log_json.get('requestBody')

    @staticmethod
    def extract_uri_from_log(log_json):
        return log_json.get('uri')

    @staticmethod
    def extract_method_from_log(log_json):
        return log_json.get('method')

    # TODO: check URLs with multiple values
    @staticmethod
    def extract_path_parameter_from_log(log_json, transition_name):
        result = {}
        if OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri')) == transition_name:
            # if the url in log and in the model has the same name, then there is not path parameter
            # example, '/login' == '/login'
            return result
        
        result = StringUtils.extract_url_value_from_url(transition_name.split('-')[1], log_json.get('uri'))
        return result
        #TODO: remove
        # transition_uri_splited = transition_name.split('-')[1].split('/')
        # log_uri_splited = log_json.get('uri').split('/')

        # if (len(transition_uri_splited) == len(log_uri_splited)):
        #     for i in range(len(transition_uri_splited)):
        #         if (transition_uri_splited[i] != log_uri_splited[i]):
        #             if ('{' in transition_uri_splited[i]):
        #                 key = transition_uri_splited[i].replace("{", "").replace("}", "")
        #                 value = log_uri_splited[i]
        #                 result[key] = value
        # else:
        #     return result
        # return result

    @staticmethod
    def create_request_response_from_log(log_json, openAPI2PetriNet=None):
            return {
                       'uri': log_json.get('uri'),
                       'method': log_json.get('method'),
                       'user_id': log_json.get('ip')
                   }, {
                       'response_body': log_json.get('responseBody'),
                       'user_id': log_json.get('ip')
                   }, log_json.get('statusCode')

    @staticmethod
    def create_response_data_from_log(log_json, parameter):
        return {
            parameter:log_json.get('responseBody').get(parameter), 
            'user_id':log_json.get('ip')
            }   