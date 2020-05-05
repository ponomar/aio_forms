import pytest

from aio_forms import SelectMultipleField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=SelectMultipleField,
        default=['1'],
        default_new=['2'],
        coerce=lambda x: x,
        has_validators=True,
        has_required=True,
    )


def test_with_default():
    options = [
        [None, 'Title'],
        ['1', 'First option'],
        ['2', 'Second option'],
        ['3', 'Third option'],
    ]
    default = ['2', '3']

    field = SelectMultipleField(
        key=FIELD_KEY,
        options=lambda: options,
        default=default,
    )
    schema = field.schema()
    assert schema['value'] == default
    assert schema['options'] == [[k_, v_, k_ in default] for k_, v_ in options]


def test_without_default():
    options = [
        [None, 'Title'],
        ['1', 'First option'],
        ['2', 'Second option'],
        ['3', 'Third option'],
    ]

    field = SelectMultipleField(key=FIELD_KEY, options=lambda: options)
    schema = field.schema()
    assert schema['value'] == []
    assert schema['options'] == [[k_, v_, False] for k_, v_ in options]


def test_without_default_with_updated_value():
    options = [
        [None, 'Title'],
        ['1', 'First option'],
        ['2', 'Second option'],
        ['3', 'Third option'],
    ]

    field = SelectMultipleField(key=FIELD_KEY, options=lambda: options)
    schema = field.schema()
    assert schema['value'] == []
    assert schema['options'] == [[k_, v_, False] for k_, v_ in options]

    value = ['2']
    field.set_value(value)
    schema = field.schema()
    assert schema['value'] == value
    assert schema['options'] == [[k_, v_, k_ == value[0]] for k_, v_ in options]


def test_with_coerce_int():
    def coerce(x):
        if x in ('', None):
            return x

        return int(x)

    options = [
        [None, 'Title'],
        ['1', 'First option'],
        ['2', 'Second option'],
        ['3', 'Third option'],
    ]
    default = ['2']

    field = SelectMultipleField(
        key=FIELD_KEY,
        options=lambda: options,
        default=default,
        coerce=coerce,
    )
    schema = field.schema()
    assert schema['value'] == [int(default[0])]
    assert schema['options'] == [
        [field.fld_coerce(k_), v_, field.fld_coerce(k_) == int(default[0])]
        for k_, v_ in options
    ]


def test_with_coerce_int_as_integers():
    def coerce(x):
        if x in ('', None):
            return x

        return int(x)

    options = [
        [None, 'Title'],
        [1, 'First option'],
        [2, 'Second option'],
        [3, 'Third option'],
    ]
    default = [2]

    field = SelectMultipleField(
        key=FIELD_KEY,
        options=lambda: options,
        default=default,
        coerce=coerce,
    )
    schema = field.schema()
    assert schema['value'] == default
    assert schema['options'] == [[k_, v_, k_ in default] for k_, v_ in options]
