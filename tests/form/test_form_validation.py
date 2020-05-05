import pytest

from aio_forms import Form, IntegerField, LengthValidator, NumberRangeValidator, StringField


pytestmark = pytest.mark.asyncio


class _Form(Form):
    field_string = StringField(
        validators=(LengthValidator(min=3, max=10),),
    )
    field_string_required = StringField(
        validators=(LengthValidator(min=5, max=50),),
        required=True,
    )
    field_integer = IntegerField(
        validators=(NumberRangeValidator(min=-10, max=10),),
    )
    field_integer_required = IntegerField(
        validators=(NumberRangeValidator(min=-10, max=10),),
        required=True,
    )


async def test_failed():
    form = _Form()
    assert await form.validate() is False
    assert form.errors.pop(form.field_string_required.key, None) is not None
    assert form.errors.pop(form.field_integer_required.key, None) is not None
    assert form.errors == {}


async def test_for_required():
    dummy = _Form()
    form = _Form({
        dummy.field_string_required.key: '1' * 10,
        dummy.field_integer_required.key: 3,
    })
    assert await form.validate() is True


async def test_failed_with_wrong_values():
    dummy = _Form()
    form = _Form({
        dummy.field_string.key: '1' * 11,
        dummy.field_string_required.key: '1' * 51,
        dummy.field_integer.key: 11,
        dummy.field_integer_required.key: -11,
    })
    assert await form.validate() is False
    assert form.errors.pop(dummy.field_string.key, None) is not None
    assert form.errors.pop(dummy.field_string_required.key, None) is not None
    assert form.errors.pop(dummy.field_integer.key, None) is not None
    assert form.errors.pop(dummy.field_integer_required.key, None) is not None
    assert form.errors == {}
