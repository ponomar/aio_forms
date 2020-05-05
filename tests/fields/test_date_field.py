from datetime import date, datetime

import pytest

from aio_forms import ERROR_NOT_VALID_DATE, ERROR_REQUIRED, DateField, coerce_date
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=DateField,
        default=date(2018, 1, 2),
        default_new=date(2018, 1, 3),
        coerce=coerce_date,
    )


async def test():
    default = date(2018, 1, 1)

    field = DateField(key=FIELD_KEY, default=default)
    assert field.value == default
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='date',
        input_type='date',
        value='2018-01-01',
        label=None,
    )


def test_bad_input():
    field = DateField(key=FIELD_KEY)
    field.set_value('1a')
    field.schema()


async def test_required():
    field = DateField(key=FIELD_KEY, required=True)
    assert field.error is None
    assert await field.validate(None) is False
    assert field.error == ERROR_REQUIRED
    field.set_value('2018-01-05')
    assert await field.validate(None) is True
    assert field.error is None
    field.set_value(date(2018, 4, 1))
    assert await field.validate(None) is True
    assert field.error is None
    field.set_value('1.0a')
    assert await field.validate(None) is False
    assert field.error == ERROR_NOT_VALID_DATE
    field.set_value(datetime(2018, 1, 1))
    assert await field.validate(None) is False
    assert field.error == ERROR_NOT_VALID_DATE


def test_value_schema():
    field = DateField(key=FIELD_KEY, required=True)
    field.set_value(date(2018, 1, 10))
    assert field.schema()['value'] == '2018-01-10'
