import pytest

from core.utils.case_convertrer import camel_case_to_snake_case


def test_camel_case_to_snake_case():
    assert camel_case_to_snake_case("SomeSDK") == "some_sdk"
    assert camel_case_to_snake_case("RServoDrive") == "r_servo_drive"
    assert camel_case_to_snake_case("SDKSome") == "sdk_some"

    assert camel_case_to_snake_case("CamelCase") == "camel_case"
    assert camel_case_to_snake_case("camelCase") == "camel_case"
    assert camel_case_to_snake_case("HTTPRequest") == "http_request"
    assert camel_case_to_snake_case("A") == "a"
    assert camel_case_to_snake_case("") == ""
