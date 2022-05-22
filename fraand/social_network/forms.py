from crispy_forms.bootstrap import Alert
from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from .models import Item, Image


from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.shortcuts import render
from django.template.loader import render_to_string


class Formset(LayoutObject):
    template = "formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})


class ItemImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'public', 'city', 'tags']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'POST'
        self.helper.form_action = 'add_item'
        self.helper.form_class = 'form-horizontal'
        self.render_required_fields = True

        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('public'),
            Field('city'),
            Field('tags'),
            Alert(content="<strong>Warning!</strong> Images are buggy a bit, please, don't remove any of it. "
                          "Adding new ones should work fine, though."),
            Fieldset('Add images', Formset('images_form')),
            Submit('submit', 'Submit'),
        )


ItemImageFormSet = inlineformset_factory(
    parent_model=Item,
    model=Image,
    form=ItemImageForm,
    fields=['image'],
    can_order=True,
    extra=3,
    can_delete=True,
    can_delete_extra=True,
    max_num=9,
    validate_max=True,
)
