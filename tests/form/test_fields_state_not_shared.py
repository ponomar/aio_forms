from aio_forms import Form, StringField


def test():
    key1, key2 = 'key1', 'key2'

    class FormClass(Form):
        field1 = StringField(key=key1)
        field2 = StringField(key=key2)

    form1 = FormClass()
    assert form1.field1.key == key1
    assert form1.field2.key == key2

    form2 = FormClass()
    assert form2.field1.key == key1
    assert form2.field2.key == key2

    key1_new, key2_new = 'key1_new', 'key2_new'
    form1.field1._set_key(key1_new)
    form1.field2._set_key(key2_new)
    assert form1.field1.key == key1_new  # new state
    assert form1.field2.key == key2_new
    assert FormClass.field1.key == key1  # old state
    assert FormClass.field2.key == key2
    assert form2.field1.key == key1      # old state
    assert form2.field2.key == key2
