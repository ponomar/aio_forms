import pytest

from aio_forms import NumberRangeValidator
from tests.fields.utils import assert_json_types
from tests.validators import DummyField


pytestmark = pytest.mark.asyncio


async def test():
    min, max, error = -100, 100.5, 'From -100 to 100.5.'

    validator = NumberRangeValidator(
        min=min,
        max=max,
        error=error,
    )
    assert validator.get_error() == error
    assert_json_types(validator.schema())
    assert validator.schema() == dict(
        type='number',
        rule='range',
        min=min,
        max=max,
        error=error,
    )
    assert await validator(None, DummyField(min - 1)) == error
    assert await validator(None, DummyField(min)) is None
    assert await validator(None, DummyField(max - 1)) is None
    assert await validator(None, DummyField(max)) is None
    assert await validator(None, DummyField(max + 1)) == error


def test_failed_arguments():
    with pytest.raises(ValueError):
        NumberRangeValidator()
    with pytest.raises(ValueError):
        NumberRangeValidator(min=1, max=1)
    with pytest.raises(ValueError):
        NumberRangeValidator(min=2, max=1)


async def test_minimal():
    min, max = 1, 2
    error_1 = 'Must be not less than %d.' % min
    error_2 = 'Must be not greater than %d.' % max

    validator_1 = NumberRangeValidator(min=min)
    assert validator_1.get_error() == error_1
    assert validator_1.schema() == dict(
        type='number',
        rule='range',
        min=min,
        error=error_1,
    )
    assert await validator_1(None, DummyField(min - 1)) == error_1
    assert await validator_1(None, DummyField(min)) is None

    validator_2 = NumberRangeValidator(max=max)
    assert validator_2.get_error() == error_2
    assert validator_2.schema() == dict(
        type='number',
        rule='range',
        max=max,
        error=error_2,
    )
