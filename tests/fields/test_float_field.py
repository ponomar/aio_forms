import pytest

from aio_forms import (
    ERROR_NOT_VALID_FLOAT,
    ERROR_REQUIRED,
    FloatField,
    NumberRangeValidator,
    coerce_float,
)
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=FloatField,
        default=1.2,
        default_new=2,
        coerce=coerce_float,
    )


async def test():
    default = 0.0

    field = FloatField(key=FIELD_KEY, default=default)
    assert field.value == default
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='float',
        input_type='number',
        value=default,
        label=None,
    )


def test_bad_input():
    field = FloatField(key=FIELD_KEY)
    field.set_value('1a')
    field.schema()


async def test_required():
    field = FloatField(key=FIELD_KEY, required=True)
    assert field.error is None
    assert await field.validate(None) is False
    assert field.error == ERROR_REQUIRED

    field.set_value('1.2')
    assert await field.validate(None) is True
    assert field.error is None

    field.set_value(1.2)
    assert field.value == 1.2
    assert await field.validate(None) is True
    assert field.error is None

    field.set_value(1)
    assert await field.validate(None) is True
    assert field.error is None

    field.set_value('1.0a')
    assert await field.validate(None) is False
    assert field.error == ERROR_NOT_VALID_FLOAT


def test_ndigits():
    field = FloatField(key=FIELD_KEY, ndigits=2)
    assert field.error is None

    field.set_value('1.2')
    assert field.value == 1.2

    field.set_value('1.223')
    assert field.value == 1.22

    field.set_value(1)
    assert field.value == 1.0

    field.set_value(1.235)
    assert field.value == 1.24


async def test_number_range_validator():
    field = FloatField(
        key=FIELD_KEY,
        validators=(NumberRangeValidator(min=-100, max=100),),
        required=True,
    )

    field.set_value('-101')  # error, too small
    assert await field.validate(None) is False

    field.set_value('-100')  # ok, bottom boundary
    await field.validate(None)
    assert await field.validate(None) is True

    field.set_value('10')  # ok
    assert await field.validate(None) is True

    field.set_value('100')  # ok, top boundary
    assert await field.validate(None) is True

    field.set_value('101')  # error, too big
    assert await field.validate(None) is False
