import pytest

from aio_forms import FileField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=FileField,
        default='   Test default    ',
        default_new='   Test default new   ',
    )


async def test():
    field = FileField(key=FIELD_KEY)
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='file',
        input_type='file',
        value=None,
        label=None,
    )
