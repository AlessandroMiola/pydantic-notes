import pytest
from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel, to_pascal


@pytest.fixture
def model_with_plain_alias():
    class ModelWithPlainAlias(BaseModel):
        first_name: str = Field(alias="firstName")

    return ModelWithPlainAlias


@pytest.fixture
def model_with_serialization_alias():
    class ModelWithSerializationAlias(BaseModel):
        first_name: str = Field(serialization_alias="f_name")

    return ModelWithSerializationAlias


@pytest.fixture
def model_with_validation_alias():
    class ModelWithValidationAlias(BaseModel):
        first_name: str = Field(validation_alias="firstName")

    return ModelWithValidationAlias


@pytest.fixture
def model_with_validation_alias_choices():
    class ModelWithValidationAliasChoices(BaseModel):
        first_name: str = Field(validation_alias=AliasChoices("firstName", "givenName", "preferredName"))

    return ModelWithValidationAliasChoices


@pytest.fixture
def model_with_validation_alias_path():
    class ModelWithValidationAliasPath(BaseModel):
        pass


@pytest.fixture
def model_with_plain_and_serialization_alias():
    class ModelWithPlainAndSerializationAlias(BaseModel):
        first_name: str = Field(alias="firstName", serialization_alias="f_name")

    return ModelWithPlainAndSerializationAlias


@pytest.fixture
def model_with_plain_and_validation_alias():
    class ModelWithPlainAndValidationAlias(BaseModel):
        first_name: str = Field(alias="f_name", validation_alias="firstName")

    return ModelWithPlainAndValidationAlias


@pytest.fixture
def model_with_plain_and_serialization_and_validation_alias():
    class ModelWithPlainAndSerializationAndValidationAlias(BaseModel):
        first_name: str = Field(alias="f_name_a", serialization_alias="f_name_s", validation_alias="firstName")

    return ModelWithPlainAndSerializationAndValidationAlias


@pytest.fixture
def model_with_plain_alias_and_pop_by_name_config():
    class ModelWithPlainAliasPopByName(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        first_name: str = Field(alias="firstName")

    return ModelWithPlainAliasPopByName


@pytest.fixture
def model_with_serialization_alias_and_pop_by_name_config():
    class ModelWithSerializationAliasPopByName(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        first_name: str = Field(serialization_alias="f_name")

    return ModelWithSerializationAliasPopByName


@pytest.fixture
def model_with_validation_alias_and_pop_by_name_config():
    class ModelWithValidationAliasPopByName(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        first_name: str = Field(validation_alias="firstName")

    return ModelWithValidationAliasPopByName


@pytest.fixture
def model_with_alias_generator_and_unset_priority():
    class ModelWithAliasGeneratorAndUnsetPriority(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(
                alias=to_camel,
                validation_alias=lambda x: x.upper(),
                serialization_alias=to_pascal,
            )
        )
        first_name_pa: str = Field(alias="f_name_pa")
        first_name_va: str = Field(validation_alias="f_name_va")
        first_name_sa: str = Field(serialization_alias="f_name_sa")

    return ModelWithAliasGeneratorAndUnsetPriority


@pytest.fixture
def model_with_alias_generator_and_priority_1():
    class ModelWithAliasGeneratorAndAliasPriority1(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(
                alias=to_camel,
                validation_alias=lambda x: x.upper(),
                serialization_alias=to_pascal,
            )
        )
        first_name_pa: str = Field(alias="f_name_pa", alias_priority=1)
        first_name_va: str = Field(validation_alias="f_name_va", alias_priority=1)
        first_name_sa: str = Field(serialization_alias="f_name_sa", alias_priority=1)

    return ModelWithAliasGeneratorAndAliasPriority1


@pytest.fixture
def model_with_alias_generator_and_priority_2():
    class ModelWithAliasGeneratorAndAliasPriority2(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(
                alias=to_camel,
                validation_alias=lambda x: x.upper(),
                serialization_alias=to_pascal,
            )
        )
        first_name_pa: str = Field(alias="f_name_pa", alias_priority=2)
        first_name_va: str = Field(validation_alias="f_name_va", alias_priority=2)
        first_name_sa: str = Field(serialization_alias="f_name_sa", alias_priority=2)

    return ModelWithAliasGeneratorAndAliasPriority2
