class StringUtils:
    # return true if the URIs are the same
    # ex: "/rest/basket/6" and "/rest/basket/{basketId}"
    @staticmethod
    def compare_uri_with_model(model_uri, uri):
        if model_uri == uri:
            return True
        #if model_uri.split(' '):
        if len(model_uri.split(' ')) > 1:
            model_uri = model_uri.split(' ')[0]
        model_uri_splited = model_uri.split('/')
        uri_splited = uri.split('/')
        if (len(model_uri_splited) == len(uri_splited)):
            for i in range(len(model_uri_splited)):
                if (model_uri_splited[i] != uri_splited[i]):
                    if not ('{' in model_uri_splited[i]):
                        return False
        else:
            return False

        return True


    @staticmethod
    def extract_url_value_from_url(model_uri, uri_with_value):
        """_summary_

        Args:
            model_uri (string): a model of a uri, example: '/accounts/{id}'
            uri (string): a concrete url, example: '/accounts/6'

        Returns:
            map: {"name_in_model" : "value_in_url"}
        """
        result = {}
        model_uri_splited = model_uri.split('/')
        uri_with_value_splited = uri_with_value.split('/')

        if (len(model_uri_splited) == len(uri_with_value_splited)):
            for i in range(len(model_uri_splited)):
                if (model_uri_splited[i] != uri_with_value_splited[i]):
                    if ('{' in model_uri_splited[i]):
                        key = model_uri_splited[i].replace("{", "").replace("}", "")
                        value = uri_with_value_splited[i]
                        result[key] = value
        else:
            return result
        return result