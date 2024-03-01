from django import forms


class AddToOrderForm(forms.Form):
    part_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
    )


class DeleteFromOrderForm(forms.Form):
    part_unit_pk = forms.IntegerField(widget=forms.HiddenInput)
