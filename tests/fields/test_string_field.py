import pytest

from aio_forms import ERROR_REQUIRED, LengthValidator, StringField
from tests.fields.utils import FIELD_KEY, do_common


pytestmark = pytest.mark.asyncio


async def test_common():
    await do_common(
        field_cls=StringField,
        default='   Test default    ',
        default_new='   Test default new   ',
        has_validators=True,
        has_filters=True,
        has_required=True,
    )


def test():
    label = 'Test Label'
    field = StringField(key=FIELD_KEY, label=lambda: label)
    assert field.schema() == dict(
        key=FIELD_KEY,
        type='string',
        input_type='text',
        value=None,
        label=label,
    )


async def test_length_validator():
    field_1 = StringField(key=FIELD_KEY, required=True)
    assert field_1.error is None
    assert await field_1.validate(None) is False
    assert field_1.error == ERROR_REQUIRED

    field_2 = StringField(key=FIELD_KEY, required=False)
    assert field_2.error is None
    assert await field_2.validate(None) is True
    assert field_2.error is None

    field_3 = StringField(key=FIELD_KEY, validators=(LengthValidator(min=5, max=10),))
    assert await field_3.validate(None) is True  # ok, because not required

    field_4 = StringField(
        key=FIELD_KEY,
        validators=(LengthValidator(min=5, max=10),),
        required=True,
    )
    assert await field_4.validate(None) is False  # required, but empty
    field_4.set_value('1' * 5)
    assert await field_4.validate(None) is True  # ok, 5-symbols text
    field_4.set_value('1' * 15)
    assert await field_4.validate(None) is False  # error, too big
    field_4.set_value('1' * 7)
    assert await field_4.validate(None) is True  # ok, 7-symbols text


def test_filters():
    default = 'Some text. Another text.   '

    field = StringField(
        key=FIELD_KEY,
        default=default,
        filters=(
            lambda x: x.lower(),
            lambda x: x.replace('a', 'b'),
        ),
    )
    assert field.value == default.strip().lower().replace('a', 'b')
