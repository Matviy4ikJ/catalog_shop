from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices={'liqpay': 'Pay with LiqPay',
                                                'monopay': 'Pay with MonoPay',
                                                'googlepay': 'Pay with Google Pay',
                                                'cash': 'With cash'
                                                }),

    class Meta:
        model = Order
        fields = ['contact_name', 'contact_email', 'contact_phone', 'address']

        labels = {'contact_name': 'Enter your name',
                  'contact_email': 'Enter your contact email',
                  'contact_phone': 'Enter your contact phone',
                  'address': 'Enter your address',
                  'payment_method': 'Payment method:'}

