import pytest

from aio_forms import Form, StringField


def test_main():
    class _Form(Form):
        field_1 = StringField()
        field_2 = StringField()
        field_3 = StringField(key='field_1')

    with pytest.raises(ValueError):
        _Form()


def test_fields_keys():
    class _Form(Form):
        field_1 = StringField()
        field_2 = StringField(key='field_3')

    form = _Form()
    assert form.field_1.key == 'field_1'
    assert form.field_2.key == 'field_3'
