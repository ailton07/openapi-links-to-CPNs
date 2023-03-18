import json
from utils.openapi_utils import OpenAPIUtils
from utils.string_utils import StringUtils


class LogUtils:
    USER_IDENTIFICATION_AUTH = 'headerAuthorization'
    USER_IDENTIFICATION_IP = 'ip'

    #USER_IDENTIFICATION = USER_IDENTIFICATION_IP
    USER_IDENTIFICATION = USER_IDENTIFICATION_AUTH

    @staticmethod
    def get_user_identification(log_json):
        if LogUtils.USER_IDENTIFICATION == LogUtils.USER_IDENTIFICATION_IP:
            return log_json.get(LogUtils.USER_IDENTIFICATION)
        else:
            if log_json.get(LogUtils.USER_IDENTIFICATION):
                return log_json.get(LogUtils.USER_IDENTIFICATION).replace('Bearer ', '')
            # this try catch is necessary to capture cases where the request doest have token
            # ex: "responseBody":{"error":{"message":"No Authorization header was found","name":"UnauthorizedError","code":"credentials_required","status":401}}
            try:
                return log_json.get('responseBody').get('authentication').get('token').replace('Bearer ', '')
            except:
                return ""


    @staticmethod
    def create_data_from_request_body_in_log(log_json, parameter):
        return {
            parameter: log_json.get('requestBody').get(parameter),
            'user_id': LogUtils.get_user_identification(log_json)
        }

    @staticmethod
    def create_data_custom_from_log(parameter, value, log_json):
        return {
            parameter: value,
            'user_id': LogUtils.get_user_identification(log_json)
        }

    @staticmethod
    def create_data_custom_from_log_with_dict(dict, log_json):
        dict['user_id'] =  LogUtils.get_user_identification(log_json)
        return dict

    @staticmethod
    def extract_http_method_with_uri_low_case(log_json):
        return OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri'), log_json.get('statusCode'))

    @staticmethod
    def extract_request_body_names_from_log(log_json):
        return [*log_json.get('requestBody').keys()]  # convert dict to array

    @staticmethod
    def extract_request_body_from_log(log_json):
        return log_json.get('requestBody')

    @staticmethod
    def extract_uri_from_log(log_json):
        uri = log_json.get('uri')
        if uri[-1] == '/':
            uri = uri[:-1]
        return str.lower(uri)

    @staticmethod
    def extract_method_from_log(log_json):
        return log_json.get('method')

    @staticmethod
    def extract_status_code_from_log(log_json):
        return log_json.get('statusCode')
    
    @staticmethod
    def extract_status_code_str_from_log(log_json):
        return str(log_json.get('statusCode'))

    # TODO: check URLs with multiple values
    @staticmethod
    def extract_path_parameter_from_log(log_json, transition_name):
        result = {}
        if OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri'), log_json.get('statusCode')) == transition_name:
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
                       'user_id': LogUtils.get_user_identification(log_json)
                   }, {
                       'response_body': log_json.get('responseBody'),
                       'user_id': LogUtils.get_user_identification(log_json)
                   }, log_json.get('statusCode')

    @staticmethod
    def create_response_data_from_log(log_json, parameter):
        return {
            parameter: log_json.get('responseBody').get(parameter), 
            'user_id': LogUtils.get_user_identification(log_json)
            }   


    @staticmethod
    def load_logs(logs_path):
        """ Read a file and returns the content parsed as json
        Case 1: Example of an accepted file with a proper format
        [{"timestamp":"2022-02-08T16:51:17.505Z"},{"timestamp":"2022-02-08T16:51:17.505Z"}]

        Case 2: Example of an accepted file with a improper format
        {"timestamp":"2022-02-08T16:51:17.505Z"}
        {"timestamp":"2022-02-08T16:51:17.505Z"}

        Args:
            logs_path (string): Path to the logs

        Returns:
            Array<Objects>: Returns an array of objects
        """
        logs_file = open(logs_path)
        try:
            logs_json = json.load(logs_file)
        except json.JSONDecodeError as exception:
            logs_file.close()
            with open(logs_path) as logs_file:
                # TODO: add to the tests this case
                logs_json = []
                for line in logs_file.readlines():
                    parsed_line_json = json.loads(line)
                    logs_json.append(parsed_line_json)
        logs_file.close()
        if isinstance(logs_json, list):
            return logs_json
        return [logs_json]