from aio_forms import Form, StringField


def get_form_main_cls():
    class FormMain(Form):
        field_s1f = StringField()
        field_d2g = StringField()
        field_a3q = StringField()
        field_v4e = StringField()
        field_k5a = StringField()
        field_j6h = StringField()
        field_r7u = StringField()
        field_e8y = StringField()
        field_l9n = StringField()
        field_t10b = StringField()

    return FormMain


def test_form_main():
    FormMain = get_form_main_cls()
    form = FormMain()

    assert len(form.fields) == 10

    for idx, field in enumerate(form.fields):
        assert field.key is not None, idx

    assert form.fields[0].key == form.field_s1f.key
    assert form.fields[1].key == form.field_d2g.key
    assert form.fields[2].key == form.field_a3q.key
    assert form.fields[3].key == form.field_v4e.key
    assert form.fields[4].key == form.field_k5a.key
    assert form.fields[5].key == form.field_j6h.key
    assert form.fields[6].key == form.field_r7u.key
    assert form.fields[7].key == form.field_e8y.key
    assert form.fields[8].key == form.field_l9n.key
    assert form.fields[9].key == form.field_t10b.key


def test_form_inherited():
    class FormInherited(get_form_main_cls()):
        field_x11p = StringField()
        field_o12s = StringField()
        field_y13z = StringField()

    form = FormInherited()

    assert len(form.fields) == 13

    for idx, field in enumerate(form.fields):
        assert field.key is not None, idx

    assert form.fields[0].key == form.field_s1f.key
    assert form.fields[1].key == form.field_d2g.key
    assert form.fields[2].key == form.field_a3q.key
    assert form.fields[3].key == form.field_v4e.key
    assert form.fields[4].key == form.field_k5a.key
    assert form.fields[5].key == form.field_j6h.key
    assert form.fields[6].key == form.field_r7u.key
    assert form.fields[7].key == form.field_e8y.key
    assert form.fields[8].key == form.field_l9n.key
    assert form.fields[9].key == form.field_t10b.key
    assert form.fields[10].key == form.field_x11p.key
    assert form.fields[11].key == form.field_o12s.key
    assert form.fields[12].key == form.field_y13z.key
