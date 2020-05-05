import pytest

from aio_forms import PasswordField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=PasswordField,
        default='   Test default    ',
        default_new='   Test default new   ',
        has_required=True,
        has_filters=True,
        has_validators=True,
    )


async def test():
    default = '   Test default    '

    field = PasswordField(key=FIELD_KEY, default=default)
    assert field.value == default.strip()
    assert await field.validate(None) is True
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='password',
        input_type='password',
        value=default.strip(),
        label=None,
    )
