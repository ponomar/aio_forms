import pytest

from aio_forms import BooleanField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=BooleanField,
        default=True,
        default_new=False,
        has_required=True,
    )


async def test_default_true():
    field = BooleanField(key=FIELD_KEY, default=True)
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='boolean',
        input_type='checkbox',
        value=True,
        label=None,
    )


async def test_default_false():
    field = BooleanField(key=FIELD_KEY, default=False)
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='boolean',
        input_type='checkbox',
        value=False,
        label=None,
    )
