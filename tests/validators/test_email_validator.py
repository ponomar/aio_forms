import pytest

from aio_forms import EmailValidator
from tests.fields.utils import assert_json_types
from tests.validators import DummyField


pytestmark = pytest.mark.asyncio


async def test():
    error = 'Invalid Email.'

    validator = EmailValidator(error)
    assert validator.get_error() == error
    schema = validator.schema()
    assert_json_types(schema)
    assert schema['type'] == 'regex'
    assert schema['error'] == error
    assert await validator(None, DummyField('')) == error
    assert await validator(None, DummyField('example.com')) == error
    assert await validator(None, DummyField('a@@example.com')) == error
    assert await validator(None, DummyField('a@b@example.com')) == error
    assert await validator(None, DummyField('a@example')) == error
    assert await validator(None, DummyField('a@example.')) == error
    assert await validator(None, DummyField('a@.com')) == error
    assert await validator(None, DummyField('a+1@b.com')) == error
    assert await validator(None, DummyField('ab c@b.com')) == error
    assert await validator(None, DummyField('abc@b c.com')) == error
    assert await validator(None, DummyField('abc@bc.c om')) == error
    assert await validator(None, DummyField('abc@bc..com')) == error
    assert await validator(None, DummyField('abcф@bc.com')) == error
    assert await validator(None, DummyField('abc@ex.am.p.l.e.com')) is None
    assert await validator(None, DummyField('abc@example.com')) is None
    assert await validator(None, DummyField('a@b.co')) is None
