import pytest

from aio_forms import EqualToValidator, Form, StringField


pytestmark = pytest.mark.asyncio

_ERROR_NOT_EQUAL = 'Error not equal.'
_ERROR_FIELD_NOT_EXISTS = 'Error field does not exist.'


def test_schema():
    validator = EqualToValidator(
        fieldname='password',
        error=_ERROR_NOT_EQUAL,
        error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
    )
    assert validator.schema() == dict(
        type='equal_to',
        fieldname='password',
        error=_ERROR_NOT_EQUAL,
    )


async def test():
    validator = EqualToValidator(
        fieldname='password',
        error=_ERROR_NOT_EQUAL,
        error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
    )

    class _Form(Form):
        password = StringField()
        password2 = StringField(validators=(validator,))

    form = _Form(dict(password='xxxxx', password2='xxxxx'))
    assert await form.validate() is True
    assert form.errors is None


async def test_error_not_equal():
    validator = EqualToValidator(
        fieldname='password',
        error=lambda: _ERROR_NOT_EQUAL,
        error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
    )

    class _Form(Form):
        password = StringField()
        password2 = StringField(validators=(validator,))

    form = _Form(dict(password='xxxxx', password2='yyyyy'))
    assert await form.validate() is False
    assert form.errors[form.password2.key] == _ERROR_NOT_EQUAL


async def test_error_field_not_exists():
    validator = EqualToValidator(
        fieldname='password3',
        error=_ERROR_NOT_EQUAL,
        error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
    )

    class _Form(Form):
        password = StringField()
        password2 = StringField(validators=(validator,))

    form = _Form(dict(password='xxxxx', password2='xxxxx'))
    assert await form.validate() is False
    assert form.errors[form.password2.key] == _ERROR_FIELD_NOT_EXISTS


async def test_error_field_not_exists_lazy_error():
    validator = EqualToValidator(
        fieldname='password3',
        error=_ERROR_NOT_EQUAL,
        error_field_not_exists=lambda: _ERROR_FIELD_NOT_EXISTS,
    )

    class _Form(Form):
        password = StringField()
        password2 = StringField(validators=(validator,))

    form = _Form(dict(password='xxxxx', password2='xxxxx'))
    assert await form.validate() is False
    assert form.errors[form.password2.key] == _ERROR_FIELD_NOT_EXISTS
