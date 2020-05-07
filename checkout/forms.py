from django import forms
from accounts.forms import ProfileForm

class PaymentDetailsForm(ProfileForm):
    cardholder = forms.CharField(max_length=50)
    field_order = ["cardholder", "address1", "address2", "city", "postcode", "country", "country"]
    
    # This form is only used to provide Stripe API with address details
    # which will be retieved through Javascript. It does not post data
    # to the database.
    # The receive_email and profile_pic fields are not required for 
    # the payment details form 
    def __init__(self, *args, **kwargs):
        super(PaymentDetailsForm, self).__init__(*args, **kwargs)
        self.fields.pop("receive_email")
        self.fields.pop("profile_pic")
