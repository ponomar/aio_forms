import pytest

from aio_forms import LengthValidator
from tests.fields.utils import assert_json_types
from tests.validators import DummyField


pytestmark = pytest.mark.asyncio


async def test():
    min, max = 1, 100
    error, error_count = 'From 1 to 100.', 'typed %d'

    validator = LengthValidator(
        min=min,
        max=max,
        error=error,
        error_count=error_count,
    )
    assert validator.get_error() == error
    assert validator.get_error(12) == '%s %s' % (error, error_count % 12)
    assert_json_types(validator.schema())
    assert validator.schema() == dict(
        type='string',
        rule='length',
        min=min,
        max=max,
        error=error,
    )
    assert await validator(None, DummyField('', required=True)) == f'{error} {error_count % 0}'
    assert await validator(None, DummyField('1' * min)) is None
    assert await validator(None, DummyField('1' * (max - 1))) is None
    assert await validator(None, DummyField('1' * max)) is None
    assert (
        await validator(None, DummyField('1' * (max + 1)))
        == f'{error} {error_count % (max + 1)}'
    )


def test_failed_arguments():
    with pytest.raises(ValueError):
        LengthValidator()
    with pytest.raises(ValueError):
        LengthValidator(min=-1)
    with pytest.raises(ValueError):
        LengthValidator(min=1, max=1)
    with pytest.raises(ValueError):
        LengthValidator(min=2, max=1)
    with pytest.raises(ValueError):
        LengthValidator(max=0)


def test_minimal():
    min, max = 1, 2

    validator_1 = LengthValidator(min=min)
    assert validator_1.get_error() == f'Must be from {min:d} symbols.'
    assert validator_1.schema() == dict(
        type='string',
        rule='length',
        min=min,
        error='Must be from %d symbols.' % min,
    )

    validator_2 = LengthValidator(max=max)
    assert  validator_2.get_error() == f'Must be up to {max:d} symbols.'
    assert validator_2.schema() == dict(
        type='string',
        rule='length',
        max=max,
        error='Must be up to %d symbols.' % max,
    )
