from openapi.openapi_utils import OpenAPIUtils


class LogUtils:
    @staticmethod
    def create_data_from_request_body_in_log(log_json, parameter):
        return {
            parameter: log_json.get('requestBody').get(parameter),
            'user_id': log_json.get('ip')
        }

    @staticmethod
    def extract_http_method_with_uri_low_case(log_json):
        return OpenAPIUtils.create_transition_name(log_json.get('method'), log_json.get('uri'))
