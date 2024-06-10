from contextlib import AbstractContextManager as ContextManager
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError


class TestValidationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "first_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'first_name': 'Mickey'}}],
            )
        ]
    )
    def test_should_instantiate_model_fields_by_validation_alias(
        self,
        model_with_validation_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            _ = model_with_validation_alias(**{arg_name: arg_value})
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    @pytest.mark.parametrize(
        "data, expectation, expected_error",
        [
            ({"firstName": "Mickey"}, does_not_raise(), None),
            ('{"firstName": "Mickey"}', does_not_raise(), None),
            (
                {"first_name": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'first_name': 'Mickey'}}]
            ),
            (
                '{"first_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'first_name': 'Mickey'}}]
            ),
        ]
    )
    def test_should_deserialize_by_validation_alias(
        self,
        model_with_validation_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            if isinstance(data, dict):
                _ = model_with_validation_alias.model_validate(data)
            else:
                _ = model_with_validation_alias.model_validate_json(data)
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    @pytest.mark.parametrize(
        "by_alias, method_choice, expected_value, unexpected_value",
        [
            (False, "dump", {"first_name": "Mickey"}, None),
            (True, "dump", {"first_name": "Mickey"}, None),
            (False, "dump", None, {"firstName": "Mickey"}),
            (True, "dump", None, {"firstName": "Mickey"}),
            (False, "dump_json", '{"first_name":"Mickey"}', None),
            (True, "dump_json", '{"first_name":"Mickey"}', None),
            (False, "dump_json", None, '{"firstName":"Mickey"}'),
            (True, "dump_json", None, '{"firstName":"Mickey"}'),
        ]
    )
    def test_should_serialize_by_field_name(
        self,
        model_with_validation_alias,
        by_alias: bool,
        method_choice: str,
        expected_value: dict | str | None,
        unexpected_value: dict | str | None,
    ):
        model = model_with_validation_alias(firstName="Mickey")
        if method_choice == "dump":
            if expected_value is not None:
                assert model.model_dump(by_alias=by_alias) == expected_value
            else:
                assert model.model_dump(by_alias=by_alias) != unexpected_value
        else:
            if expected_value is not None:
                assert model.model_dump_json(by_alias=by_alias) == expected_value
            else:
                assert model.model_dump_json(by_alias=by_alias) != unexpected_value


    def test_should_repr_by_field_name(self, model_with_validation_alias):
        model = model_with_validation_alias(firstName="Mickey")
        assert repr(model).find("first_name") > -1
        assert repr(model).find("firstName") == -1
        assert list(model.__rich_repr__()) == [("first_name", "Mickey")]


    @pytest.mark.parametrize(
        "arg_name, expected",
        [
            ("first_name", True),
            ("firstName", False)
        ]
    )
    def test_should_class_attribute_have_field_name(
        self,
        model_with_validation_alias,
        arg_name: str,
        expected: bool
    ):
        model = model_with_validation_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected


    def test_alias_choices(self, model_with_validation_alias_choices):
        pass


class TestValidationAliasPopByName:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            ("first_name", "Mickey", does_not_raise(), None),
            (
                "f_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'f_name': 'Mickey'}}],
            )
        ]
    )
    def test_instantiate_model_fields_by_field_name_or_validation_alias(
        self,
        model_with_validation_alias_and_pop_by_name_config,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            _ = model_with_validation_alias_and_pop_by_name_config(**{arg_name: arg_value})
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    @pytest.mark.parametrize(
        "data, expectation, expected_error",
        [
            ({"firstName": "Mickey"}, does_not_raise(), None),
            ('{"firstName": "Mickey"}', does_not_raise(), None),
            ({"first_name": "Mickey"}, does_not_raise(), None),
            ('{"first_name": "Mickey"}', does_not_raise(), None),
            (
                {"f_name": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
            (
                '{"f_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
        ]
    )
    def test_deserialize_by_field_name_or_validation_alias(
        self,
        model_with_validation_alias_and_pop_by_name_config,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            if isinstance(data, dict):
                _ = model_with_validation_alias_and_pop_by_name_config.model_validate(data)
            else:
                _ = model_with_validation_alias_and_pop_by_name_config.model_validate_json(data)
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    @pytest.mark.parametrize(
        "by_alias, method_choice, expected_value, unexpected_value",
        [
            (False, "dump", {"first_name": "Mickey"}, None),
            (True, "dump", {"first_name": "Mickey"}, None),
            (False, "dump", None, {"firstName": "Mickey"}),
            (True, "dump", None, {"firstName": "Mickey"}),
            (False, "dump_json", '{"first_name":"Mickey"}', None),
            (True, "dump_json", '{"first_name":"Mickey"}', None),
            (False, "dump_json", None, '{"firstName":"Mickey"}'),
            (True, "dump_json", None, '{"firstName":"Mickey"}'),
        ]
    )
    def test_should_serialize_by_field_name(
        self,
        model_with_validation_alias_and_pop_by_name_config,
        by_alias: bool,
        method_choice: str,
        expected_value: dict | str | None,
        unexpected_value: dict | str | None,
    ):
        model = model_with_validation_alias_and_pop_by_name_config(firstName="Mickey")
        if method_choice == "dump":
            if expected_value is not None:
                assert model.model_dump(by_alias=by_alias) == expected_value
            else:
                assert model.model_dump(by_alias=by_alias) != unexpected_value
        else:
            if expected_value is not None:
                assert model.model_dump_json(by_alias=by_alias) == expected_value
            else:
                assert model.model_dump_json(by_alias=by_alias) != unexpected_value


    def test_should_repr_by_field_name(self, model_with_validation_alias_and_pop_by_name_config):
        model = model_with_validation_alias_and_pop_by_name_config(firstName="Mickey")
        assert repr(model).find("first_name") > -1
        assert repr(model).find("firstName") == -1
        assert list(model.__rich_repr__()) == [("first_name", "Mickey")]


    @pytest.mark.parametrize(
        "arg_name, expected",
        [
            ("first_name", True),
            ("firstName", False)
        ]
    )
    def test_should_class_attribute_have_field_name(
        self,
        model_with_validation_alias_and_pop_by_name_config,
        arg_name: str,
        expected: bool
    ):
        model = model_with_validation_alias_and_pop_by_name_config(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected
