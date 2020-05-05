import pytest

from aio_forms import TextAreaField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=TextAreaField,
        default='   Test default    ',
        default_new='   Test default new   ',
        has_validators=True,
        has_filters=True,
        has_required=True,
    )


async def test():
    default = '   Test default    '

    field = TextAreaField(key=FIELD_KEY, default=default)
    assert field.value == default.strip()
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='text',
        input_type='textarea',
        value=default.strip(),
        label=None,
    )


def test_minimal():
    field = TextAreaField(key=FIELD_KEY)
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='text',
        input_type='textarea',
        value=None,
        label=None,
    )
