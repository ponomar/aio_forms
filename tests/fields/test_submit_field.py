import pytest

from aio_forms import SubmitField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(SubmitField)


def test():
    field = SubmitField(key=FIELD_KEY)
    assert field.value is None
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='submit',
        input_type='submit',
        value=None,
        label=None,
    )
