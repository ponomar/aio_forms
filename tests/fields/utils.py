import json

import pytest

from aio_forms import ERROR_REQUIRED, Field


def assert_json_types(data):
    assert data == json.loads(json.dumps(data))


FIELD_KEY = 'test-key'


def _do_label(field: Field):
    assert field.label is None

    label = 'Test label'
    field.set_label(lambda: label)
    assert field.label == label

    label_new = f'{label} new'
    field.set_label(label_new)
    assert field.label == label_new


def _do_default(field: Field, default, default_new):
    assert field.default is None

    field.set_default(lambda: default)
    assert field.default == default

    field.set_default(default_new)
    assert field.value == field.fld_coerce(default_new)
    field.set_default(None)  # cleanup


def _do_coerce(field: Field, coerce):
    field.set_coerce(coerce)
    assert field.fld_coerce is coerce

    coerce_new = lambda x: coerce(x)
    field.set_coerce(coerce_new)
    assert field.fld_coerce is coerce_new


def _do_validators(field: Field):
    assert field.fld_validators is None

    validators = (1, 2, 3)
    field.set_validators(validators)
    assert field.fld_validators == validators

    validators_new = (4, 5, 6)
    field.set_validators(validators_new)
    assert field.fld_validators == validators_new
    field.set_validators(None)  # cleanup


def _do_filters(field: Field):
    assert field.fld_filters is None

    filters = (1, 2, 3)
    field.set_filters(filters)
    assert field.fld_filters == filters

    filters_new = (4, 5, 6)
    field.set_filters(filters_new)
    assert field.fld_filters == filters_new
    field.set_filters(None)  # cleanup


async def _do_required(field: Field):
    assert field.required is False
    assert await field.validate(None) is True
    schema = field.schema()
    assert 'required' not in schema
    assert 'required_error' not in schema

    field.set_required(True)
    assert field.required is True
    assert field.schema()['required'] is True
    assert await field.validate(None) is False
    schema = field.schema()
    assert schema['required'] is True
    assert schema['required_error'] == ERROR_REQUIRED

    required_error = 'Required Error'
    field.set_required_error(required_error)
    assert field.get_required_error() == required_error

    required_error_new = '%s new' % required_error
    field.set_required_error(lambda: required_error_new)
    assert field.get_required_error() == required_error_new


def _do_key_absent(field_cls):
    field = field_cls()
    with pytest.raises(ValueError):
        field.schema()


async def _do_minimal(field_cls):
    field_minimal = field_cls(key=FIELD_KEY)
    assert await field_minimal.validate(None) is True
    assert_json_types(field_minimal.schema())


def _do_params(field: Field):
    assert field.params == {}

    params = dict(help='Test help', description='Test Description')
    field.set_params(params)
    assert field.params == params

    params_new = dict(help='Test help new')
    field.set_params(params_new)
    assert field.params == params_new

    params_not_valid_keys = {12: 'test'}
    with pytest.raises(TypeError):
        field.set_params(params_not_valid_keys)

    params_not_valid_type = []
    with pytest.raises(TypeError):
        field.set_params(params_not_valid_type)


async def do_common(field_cls, default=None, default_new=None, has_validators=False,
                    has_filters=False, has_required=False, coerce=None):
    field = field_cls(key=FIELD_KEY)
    assert field.key == FIELD_KEY
    assert_json_types(field.schema())

    _do_label(field)
    _do_params(field)
    _do_key_absent(field_cls)
    await _do_minimal(field_cls)

    if coerce is not None:
        _do_coerce(field, coerce)
    if default_new is not None:
        _do_default(field, default, default_new)
    if has_validators:
        _do_validators(field)
    if has_filters:
        _do_filters(field)
    if has_required:
        await _do_required(field)
