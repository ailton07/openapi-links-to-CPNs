import json

USER_IDENTIFICATION = 'user_id'


class ColouredToken:
    json_dict = None
    user_id = None

    def __init__(self, value):
        self.json_dict = json.dumps(value, separators=(',\n', ':'))
        self.user_id = value.get(USER_IDENTIFICATION)

    def __str__(self):
        return self.json_dict

    def __repr__(self):
        return self.__str__() if len(self.__str__()) < 60 else self.__str__()[0:60:1] + '...'

    def __eq__(self, other):
        if self.__str__() == other.__str__():
            return True
        return False

    def __hash__(self):
        return hash(self.json_dict)

    def get_dict(self):
        return json.loads(self.json_dict)


class RequestResponseToken(ColouredToken):
    # request data
    uri = None
    method = None
    # user_id is in ColouredToken
    # response data
    response_body = None
    status_code = None

    # def __init__ (self, json_dict, response) :
    #     self.response_body = json.dumps(response)
    #     super().__init__(json_dict)

    def __init__ (self, json_dict, response, status) :
        self.response_body = json.dumps(response, separators=(',\n', ':'))
        self.status_code = status
        self.uri = json_dict.get('uri')
        self.method = json_dict.get('method')
        super().__init__(json_dict)
        
    def get_response_body_dict (self):
        return json.loads(self.response_body)

    def get_object_from_response_body_dict (self):
        return json.loads(self.response_body).get('response_body')

    def _get_from_reponse_body (self, element):
        """
        Given an element, get the value associated in the self.response_body

        Args:
            element (string): the indication of the data we are looking for 
            ex: simple element 'id'
                composed element 'authentication.id', 

        Returns:
            pair(key, response): key is the element, when it is simple, 
            and it is the last element part when it is composed
            the response is the value in self.response_body in string format
            ex: 'id', "6"
        """
        if len(str.split(element, '.')) > 1 :
            response = json.loads(self.response_body)['response_body']
            for splited_element in str.split(element, '.'):
                key = splited_element
                response = response.get(splited_element)
            return key, str(response)
        return element, str(json.loads(self.response_body).get('response_body').get(element))

    def _get_key_value_from_response_body(self, element, new_name=None):
        key, response = self._get_from_reponse_body(element)
        if new_name:
            return {new_name : response}
        else:
            return {key : response}

    def get_token_from_reponse_body (self, element, new_name=None):
        result = self._get_key_value_from_response_body (element, new_name)
        result[USER_IDENTIFICATION] = self.user_id
        return ColouredToken(result)

    def get_status(self):
        response = {
            'status' : self.status_code,
            USER_IDENTIFICATION: self.user_id
        }
        return json.dumps(response, separators=(',\n', ':'))

    def get_response(self):
        body = json.loads(self.response_body)
        return json.dumps(body.get('response_body'), separators=(',\n', ':'))

    def _create_request_line(self, uri_str, method_str, ip_str):
        return ColouredToken({
            'uri': uri_str,
            'method': method_str,
            'user_id': ip_str
        })

    def get_next_request(self, uri_str, method_str):
        if self.uri is None:
            raise Exception("This token don't have request information")
        next_request = self._create_request_line(uri_str, method_str, self.user_id)
        return next_request