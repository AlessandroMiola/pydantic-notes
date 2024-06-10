from contextlib import AbstractContextManager as ContextManager
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError


class TestPlainAndSerializationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'f_name': 'Mickey'}}],
            ),
            (
                "first_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'first_name': 'Mickey'}}],
            )
        ]
    )
    def test_should_instantiate_model_fields_by_plain_alias(
        self,
        model_with_plain_and_serialization_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            _ = model_with_plain_and_serialization_alias(**{arg_name: arg_value})
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
                {"f_name": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
            (
                '{"f_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
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
    def test_should_deserialize_by_plain_alias(
        self,
        model_with_plain_and_serialization_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            if isinstance(data, dict):
                _ = model_with_plain_and_serialization_alias.model_validate(data)
            else:
                _ = model_with_plain_and_serialization_alias.model_validate_json(data)
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    def test_serialize_by_field_name(self, model_with_plain_and_serialization_alias):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert model.model_dump() == {"first_name": "Mickey"}
        assert model.model_dump_json() == '{"first_name":"Mickey"}'
        assert model.model_dump() != {"f_name": "Mickey"}
        assert model.model_dump_json() != '{"f_name":"Mickey"}'
        assert model.model_dump() != {"firstName": "Mickey"}
        assert model.model_dump_json() != '{"firstName":"Mickey"}'


    def test_serialize_by_serialization_alias(self, model_with_plain_and_serialization_alias):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert model.model_dump(by_alias=True) == {"f_name": "Mickey"}
        assert model.model_dump_json(by_alias=True) == '{"f_name":"Mickey"}'
        assert model.model_dump(by_alias=True) != {"first_name": "Mickey"}
        assert model.model_dump_json(by_alias=True) != '{"first_name":"Mickey"}'
        assert model.model_dump(by_alias=True) != {"firstName": "Mickey"}
        assert model.model_dump_json(by_alias=True) != '{"firstName":"Mickey"}'


    def test_should_repr_by_field_name(self, model_with_plain_and_serialization_alias):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert repr(model).find("first_name") > -1
        assert repr(model).find("f_name") == -1
        assert repr(model).find("firstName") == -1
        assert list(model.__rich_repr__()) == [("first_name", "Mickey")]


    @pytest.mark.parametrize(
        "arg_name, expected",
        [
            ("first_name", True),
            ("f_name", False),
            ("firstName", False)
        ]
    )
    def test_should_class_attribute_have_field_name(
        self,
        model_with_plain_and_serialization_alias,
        arg_name: str,
        expected: bool
    ):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected


class TestPlainAndValidationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'f_name': 'Mickey'}}],
            ),
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
        model_with_plain_and_validation_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            _ = model_with_plain_and_validation_alias(**{arg_name: arg_value})
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
                {"f_name": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
            (
                '{"f_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name': 'Mickey'}}]
            ),
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
        model_with_plain_and_validation_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            if isinstance(data, dict):
                _ = model_with_plain_and_validation_alias.model_validate(data)
            else:
                _ = model_with_plain_and_validation_alias.model_validate_json(data)
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    def test_serialize_by_field_name(self, model_with_plain_and_validation_alias):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert model.model_dump() == {"first_name": "Mickey"}
        assert model.model_dump_json() == '{"first_name":"Mickey"}'
        assert model.model_dump() != {"f_name": "Mickey"}
        assert model.model_dump_json() != '{"f_name":"Mickey"}'
        assert model.model_dump() != {"firstName": "Mickey"}
        assert model.model_dump_json() != '{"firstName":"Mickey"}'


    def test_serialize_by_serialization_alias(self, model_with_plain_and_validation_alias):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert model.model_dump(by_alias=True) == {"f_name": "Mickey"}
        assert model.model_dump_json(by_alias=True) == '{"f_name":"Mickey"}'
        assert model.model_dump(by_alias=True) != {"firstName": "Mickey"}
        assert model.model_dump_json(by_alias=True) != '{"firstName":"Mickey"}'


    def test_should_repr_by_field_name(self, model_with_plain_and_validation_alias):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert repr(model).find("first_name") > -1
        assert repr(model).find("f_name") == -1
        assert repr(model).find("firstName") == -1
        assert list(model.__rich_repr__()) == [("first_name", "Mickey")]


    @pytest.mark.parametrize(
        "arg_name, expected",
        [
            ("first_name", True),
            ("f_name", False),
            ("firstName", False)
        ]
    )
    def test_should_class_attribute_have_field_name(
        self,
        model_with_plain_and_validation_alias,
        arg_name: str,
        expected: bool
    ):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected


class TestPlainAndSerializationAndValidationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name_a",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'f_name_a': 'Mickey'}}],
            ),
            (
                "f_name_s",
                "Mickey",
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required','input': {'f_name_s': 'Mickey'}}],
            )
        ]
    )
    def test_should_instantiate_model_fields_by_validation_alias(
        self,
        model_with_plain_and_serialization_and_validation_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            _ = model_with_plain_and_serialization_and_validation_alias(**{arg_name: arg_value})
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
                {"f_name_a": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name_a': 'Mickey'}}]
            ),
            (
                '{"f_name_a": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name_a': 'Mickey'}}]
            ),
            (
                {"f_name_s": "Mickey"},
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name_s': 'Mickey'}}]
            ),
            (
                '{"f_name_s": "Mickey"}',
                pytest.raises(ValidationError),
                [{'type': 'missing', 'loc': ('firstName',), 'msg': 'Field required', 'input': {'f_name_s': 'Mickey'}}]
            ),
        ]
    )
    def test_should_deserialize_by_validation_alias(
        self,
        model_with_plain_and_serialization_and_validation_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None
    ):
        with expectation as exc_info:
            if isinstance(data, dict):
                _ = model_with_plain_and_serialization_and_validation_alias.model_validate(data)
            else:
                _ = model_with_plain_and_serialization_and_validation_alias.model_validate_json(data)
        if expected_error is None:
            assert exc_info is None
        else:
            assert exc_info is not None
            assert exc_info.value.errors(include_url=False) == expected_error


    def test_serialize_by_field_name(self, model_with_plain_and_serialization_and_validation_alias):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert model.model_dump() == {"first_name": "Mickey"}
        assert model.model_dump_json() == '{"first_name":"Mickey"}'
        assert model.model_dump() != {"f_name_a": "Mickey"}
        assert model.model_dump_json() != '{"f_name_a":"Mickey"}'
        assert model.model_dump() != {"f_name_s": "Mickey"}
        assert model.model_dump_json() != '{"f_name_s":"Mickey"}'
        assert model.model_dump() != {"firstName": "Mickey"}
        assert model.model_dump_json() != '{"firstName":"Mickey"}'


    def test_serialize_by_serialization_alias(self, model_with_plain_and_serialization_and_validation_alias):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert model.model_dump(by_alias=True) == {"f_name_s": "Mickey"}
        assert model.model_dump_json(by_alias=True) == '{"f_name_s":"Mickey"}'
        assert model.model_dump(by_alias=True) != {"firstName": "Mickey"}
        assert model.model_dump_json(by_alias=True) != '{"firstName":"Mickey"}'
        assert model.model_dump(by_alias=True) != {"f_name_a": "Mickey"}
        assert model.model_dump_json(by_alias=True) != '{"f_name_a":"Mickey"}'


    def test_should_repr_by_field_name(self, model_with_plain_and_serialization_and_validation_alias):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert repr(model).find("first_name") > -1
        assert repr(model).find("f_name_a") == -1
        assert repr(model).find("f_name_s") == -1
        assert repr(model).find("firstName") == -1
        assert list(model.__rich_repr__()) == [("first_name", "Mickey")]


    @pytest.mark.parametrize(
        "arg_name, expected",
        [
            ("first_name", True),
            ("f_name_a", False),
            ("f_name_s", False),
            ("firstName", False)
        ]
    )
    def test_should_class_attribute_have_field_name(
        self,
        model_with_plain_and_serialization_and_validation_alias,
        arg_name: str,
        expected: bool
    ):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected
