import pytest
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


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
