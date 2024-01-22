from django import forms

from user.models import ShippingAddress


class AddToOrderForm(forms.Form):
    part_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
    )


class DeleteFromOrderForm(forms.Form):
    part_unit_pk = forms.IntegerField(widget=forms.HiddenInput)


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'phone_number', 'region', 'city', 'office_number']
