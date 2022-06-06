from utils.openapi_utils import OpenAPIUtils


class LogUtils:
    @staticmethod
    def create_data_from_request_body_in_log(log_json, parameter):
        return {
            parameter: log_json.get('requestBody').get(parameter),
            'user_id': log_json.get('ip')
        }

    @staticmethod
    def create_data_from_query_parameter_in_log(parameter, value, log_json):
        return {
            parameter: value,
            'user_id': log_json.get('ip')
        }

    @staticmethod
    def extract_http_method_with_uri_low_case(log_json):
        return OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri'))

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