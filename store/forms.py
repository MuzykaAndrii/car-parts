from django import forms

class AddToOrderForm(forms.Form):
    part_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
    )
