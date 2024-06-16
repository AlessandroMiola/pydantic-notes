from contextlib import AbstractContextManager as ContextManager
from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import AliasGenerator, ValidationError
from pydantic.alias_generators import to_camel, to_pascal


class TestPlainAndSerializationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                "first_name",
                "Mickey",
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
        ],
    )
    def test_should_instantiate_model_fields_by_plain_alias(
        self,
        model_with_plain_and_serialization_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                '{"f_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                {"first_name": "Mickey"},
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
            (
                '{"first_name": "Mickey"}',
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
        ],
    )
    def test_should_deserialize_by_plain_alias(
        self,
        model_with_plain_and_serialization_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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

    @pytest.mark.parametrize("arg_name, expected", [("first_name", True), ("f_name", False), ("firstName", False)])
    def test_should_class_attribute_have_field_name(
        self, model_with_plain_and_serialization_alias, arg_name: str, expected: bool
    ):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected

    def test_alias_priority(self, model_with_plain_and_serialization_alias):
        model = model_with_plain_and_serialization_alias(firstName="Mickey")
        assert model.model_fields["first_name"].alias_priority == 2


class TestPlainAndValidationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name",
                "Mickey",
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                "first_name",
                "Mickey",
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
        ],
    )
    def test_should_instantiate_model_fields_by_validation_alias(
        self,
        model_with_plain_and_validation_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                '{"f_name": "Mickey"}',
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name": "Mickey"}}],
            ),
            (
                {"first_name": "Mickey"},
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
            (
                '{"first_name": "Mickey"}',
                pytest.raises(ValidationError),
                [
                    {
                        "type": "missing",
                        "loc": ("firstName",),
                        "msg": "Field required",
                        "input": {"first_name": "Mickey"},
                    }
                ],
            ),
        ],
    )
    def test_should_deserialize_by_validation_alias(
        self,
        model_with_plain_and_validation_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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

    @pytest.mark.parametrize("arg_name, expected", [("first_name", True), ("f_name", False), ("firstName", False)])
    def test_should_class_attribute_have_field_name(
        self, model_with_plain_and_validation_alias, arg_name: str, expected: bool
    ):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected

    def test_alias_priority(self, model_with_plain_and_validation_alias):
        model = model_with_plain_and_validation_alias(firstName="Mickey")
        assert model.model_fields["first_name"].alias_priority == 2


class TestPlainAndSerializationAndValidationAlias:
    @pytest.mark.parametrize(
        "arg_name, arg_value, expectation, expected_error",
        [
            ("firstName", "Mickey", does_not_raise(), None),
            (
                "f_name_a",
                "Mickey",
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_a": "Mickey"}}],
            ),
            (
                "f_name_s",
                "Mickey",
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_s": "Mickey"}}],
            ),
        ],
    )
    def test_should_instantiate_model_fields_by_validation_alias(
        self,
        model_with_plain_and_serialization_and_validation_alias,
        arg_name: str,
        arg_value: str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_a": "Mickey"}}],
            ),
            (
                '{"f_name_a": "Mickey"}',
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_a": "Mickey"}}],
            ),
            (
                {"f_name_s": "Mickey"},
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_s": "Mickey"}}],
            ),
            (
                '{"f_name_s": "Mickey"}',
                pytest.raises(ValidationError),
                [{"type": "missing", "loc": ("firstName",), "msg": "Field required", "input": {"f_name_s": "Mickey"}}],
            ),
        ],
    )
    def test_should_deserialize_by_validation_alias(
        self,
        model_with_plain_and_serialization_and_validation_alias,
        data: dict | str,
        expectation: ContextManager,
        expected_error: list[dict] | None,
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
        "arg_name, expected", [("first_name", True), ("f_name_a", False), ("f_name_s", False), ("firstName", False)]
    )
    def test_should_class_attribute_have_field_name(
        self, model_with_plain_and_serialization_and_validation_alias, arg_name: str, expected: bool
    ):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert hasattr(model, arg_name) is expected
        assert (arg_name in dict(model)) is expected

    def test_alias_priority(self, model_with_plain_and_serialization_and_validation_alias):
        model = model_with_plain_and_serialization_and_validation_alias(firstName="Mickey")
        assert model.model_fields["first_name"].alias_priority == 2


class TestAliasGeneratorUnsetAliasPriority:
    @pytest.mark.parametrize(
        "field_name, plain_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_pa",
                "f_name_pa",
                AliasGenerator(alias=to_camel("first_name_pa")).alias,
                AliasGenerator(validation_alias="first_name_pa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_pa")).serialization_alias,
            ),
        ],
    )
    def test_should_plain_alias_with_unset_priority_override_generated_aliases(
        self,
        model_with_alias_generator_and_unset_priority,
        field_name: str,
        plain_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].alias == plain_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].validation_alias == plain_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].serialization_alias == plain_alias

        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].alias != gen_plain_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].validation_alias != gen_val_alias
        assert (
            model_with_alias_generator_and_unset_priority.model_fields[field_name].serialization_alias != gen_ser_alias
        )

    @pytest.mark.parametrize(
        "field_name, val_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_va",
                "f_name_va",
                AliasGenerator(alias=to_camel("first_name_va")).alias,
                AliasGenerator(validation_alias="first_name_va".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_va")).serialization_alias,
            ),
        ],
    )
    def test_should_val_alias_with_unset_priority_override_generated_val_alias(
        self,
        model_with_alias_generator_and_unset_priority,
        field_name: str,
        val_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].validation_alias == val_alias
        assert (
            model_with_alias_generator_and_unset_priority.model_fields[field_name].serialization_alias == gen_ser_alias
        )

        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].validation_alias != gen_val_alias

    @pytest.mark.parametrize(
        "field_name, ser_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_sa",
                "f_name_sa",
                AliasGenerator(alias=to_camel("first_name_sa")).alias,
                AliasGenerator(validation_alias="first_name_sa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_sa")).serialization_alias,
            ),
        ],
    )
    def test_should_ser_alias_with_unset_priority_override_generated_ser_alias(
        self,
        model_with_alias_generator_and_unset_priority,
        field_name: str,
        ser_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].validation_alias == gen_val_alias
        assert model_with_alias_generator_and_unset_priority.model_fields[field_name].serialization_alias == ser_alias

        assert (
            model_with_alias_generator_and_unset_priority.model_fields[field_name].serialization_alias != gen_ser_alias
        )


class TestAliasGeneratorAliasPriority1:
    @pytest.mark.parametrize(
        "field_name, plain_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_pa",
                "f_name_pa",
                AliasGenerator(alias=to_camel("first_name_pa")).alias,
                AliasGenerator(validation_alias="first_name_pa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_pa")).serialization_alias,
            ),
        ],
    )
    def test_should_plain_alias_with_low_priority_be_overriden_by_generated_plain_alias(
        self,
        model_with_alias_generator_and_priority_1,
        field_name: str,
        plain_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].validation_alias == gen_val_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].serialization_alias == gen_ser_alias

        assert model_with_alias_generator_and_priority_1.model_fields[field_name].alias != plain_alias

    @pytest.mark.parametrize(
        "field_name, val_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_va",
                "f_name_va",
                AliasGenerator(alias=to_camel("first_name_va")).alias,
                AliasGenerator(validation_alias="first_name_va".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_va")).serialization_alias,
            ),
        ],
    )
    def test_should_val_alias_with_low_priority_be_overriden_by_generated_val_alias(
        self,
        model_with_alias_generator_and_priority_1,
        field_name: str,
        val_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].validation_alias == gen_val_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].serialization_alias == gen_ser_alias

        assert model_with_alias_generator_and_priority_1.model_fields[field_name].validation_alias != val_alias

    @pytest.mark.parametrize(
        "field_name, ser_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_sa",
                "f_name_sa",
                AliasGenerator(alias=to_camel("first_name_sa")).alias,
                AliasGenerator(validation_alias="first_name_sa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_sa")).serialization_alias,
            ),
        ],
    )
    def test_should_ser_alias_with_low_priority_be_overridden_by_generated_ser_alias(
        self,
        model_with_alias_generator_and_priority_1,
        field_name: str,
        ser_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].validation_alias == gen_val_alias
        assert model_with_alias_generator_and_priority_1.model_fields[field_name].serialization_alias == gen_ser_alias

        assert model_with_alias_generator_and_priority_1.model_fields[field_name].serialization_alias != ser_alias


class TestAliasGeneratorAliasPriority2:
    @pytest.mark.parametrize(
        "field_name, plain_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_pa",
                "f_name_pa",
                AliasGenerator(alias=to_camel("first_name_pa")).alias,
                AliasGenerator(validation_alias="first_name_pa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_pa")).serialization_alias,
            ),
        ],
    )
    def test_should_plain_alias_with_high_priority_override_generated_aliases(
        self,
        model_with_alias_generator_and_priority_2,
        field_name: str,
        plain_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].alias == plain_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].validation_alias == plain_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].serialization_alias == plain_alias

        assert model_with_alias_generator_and_priority_2.model_fields[field_name].alias != gen_plain_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].validation_alias != gen_val_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].serialization_alias != gen_ser_alias

    @pytest.mark.parametrize(
        "field_name, val_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_va",
                "f_name_va",
                AliasGenerator(alias=to_camel("first_name_va")).alias,
                AliasGenerator(validation_alias="first_name_va".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_va")).serialization_alias,
            ),
        ],
    )
    def test_should_val_alias_with_high_priority_override_generated_val_alias(
        self,
        model_with_alias_generator_and_priority_2,
        field_name: str,
        val_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].validation_alias == val_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].serialization_alias == gen_ser_alias

        assert model_with_alias_generator_and_priority_2.model_fields[field_name].validation_alias != gen_val_alias

    @pytest.mark.parametrize(
        "field_name, ser_alias, gen_plain_alias, gen_val_alias, gen_ser_alias",
        [
            (
                "first_name_sa",
                "f_name_sa",
                AliasGenerator(alias=to_camel("first_name_sa")).alias,
                AliasGenerator(validation_alias="first_name_sa".upper()).validation_alias,
                AliasGenerator(serialization_alias=to_pascal("first_name_sa")).serialization_alias,
            ),
        ],
    )
    def test_should_ser_alias_with_high_priority_override_generated_ser_alias(
        self,
        model_with_alias_generator_and_priority_2,
        field_name: str,
        ser_alias: str,
        gen_plain_alias: str,
        gen_val_alias: str,
        gen_ser_alias: str,
    ):
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].alias == gen_plain_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].validation_alias == gen_val_alias
        assert model_with_alias_generator_and_priority_2.model_fields[field_name].serialization_alias == ser_alias

        assert model_with_alias_generator_and_priority_2.model_fields[field_name].serialization_alias != gen_ser_alias
