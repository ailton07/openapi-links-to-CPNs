class StringUtils:
    # return true if the URIs are the same
    # ex: "/rest/basket/6" and "/rest/basket/{basketId}"
    @staticmethod
    def compare_uri_with_model(model_uri, uri):
        if model_uri.split(' '):
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