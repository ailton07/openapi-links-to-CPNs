from utils.string_utils import StringUtils


def test_compare_uri_with_model_with_equivalent_uris():
    # given 2 equivalent uris
    model_uri = "/rest/basket/{basketId}"
    log_uri = "/rest/basket/6"

    # when we call compare_uri_with_model()
    result = StringUtils.compare_uri_with_model(model_uri, log_uri)

    # then we should receive True
    assert result is True


def test_compare_uri_with_model_with_different_uris():
    # given 2 different uris
    model_uri = "/rest/basket/{basketId}"
    log_uri = "/rest/user/6"

    # when we call compare_uri_with_model()
    result = StringUtils.compare_uri_with_model(model_uri, log_uri)

    # then we should receive False
    assert result is False
