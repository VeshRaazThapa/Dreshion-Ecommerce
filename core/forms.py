from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from core.models import Profile,SKIN_TONE_CHOICES,UNDER_TONE_CHOICES,GENDER_CHOICES
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re


User = get_user_model()
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user',
            'hip',
            'height',
            'high_hip',
            'bust',
            'waist',
            'skin_tone',
            'under_tone',
            'gender',
            'picture',
            'front_image',
            'back_image',
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['middle_name'].widget.attrs['class'] = "form-control"
    #     self.fields['citizenship_number'].widget.attrs['class'] = "form-control"
    #     self.fields['house_number'].widget.attrs['class'] = "form-control"
    #     self.fields['gender'].widget.attrs['class'] = "form-control"
    #     self.fields['phone'].widget.attrs['class'] = "form-control"

class UserCreationForm(forms.Form):

    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    hip = forms.DecimalField(max_digits=5, decimal_places=2,required=False,initial=12)
    height = forms.DecimalField(max_digits=5, decimal_places=2,required=False,initial=35)
    high_hip = forms.DecimalField(max_digits=5, decimal_places=2,required=False,initial=34)
    bust = forms.DecimalField(max_digits=5, decimal_places=2,required=False,initial=35)
    waist = forms.DecimalField(max_digits=5, decimal_places=2,required=False,initial=31)
    skin_tone = forms.ChoiceField(choices=SKIN_TONE_CHOICES, widget=forms.Select)

    under_tone = forms.ChoiceField(choices=UNDER_TONE_CHOICES, widget=forms.Select)

    gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.Select)
    picture = forms.ImageField( required=False)
    front_image = forms.ImageField(required=False)
    back_image = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('User already exists.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if not password1 == password2:
            raise ValidationError({"password2": "Passwords don't match."})

        if not len(password1) >= 8:
            raise ValidationError({"password1": "Password must be at least 8 characters long."})

        pattern = re.compile(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError(
                {"password1": "Password must contain alphabet characters, special characters and numbers"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control"
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password"
        self.fields['hip'].widget.attrs['class'] = "form-control"
        self.fields['hip'].widget.attrs['placeholder'] = "Enter your Hip size (cm)"
        self.fields['height'].widget.attrs['class'] = "form-control"
        self.fields['height'].widget.attrs['placeholder'] = "Enter your height (cm)"
        self.fields['high_hip'].widget.attrs['class'] = "form-control"
        self.fields['high_hip'].widget.attrs['placeholder'] = "Enter your high hip size (cm)"
        self.fields['bust'].widget.attrs['class'] = "form-control"
        self.fields['bust'].widget.attrs['placeholder'] = "Enter your bust size (cm)"
        self.fields['waist'].widget.attrs['class'] = "form-control"
        self.fields['waist'].widget.attrs['placeholder'] = "Enter your waist size (cm)"
        self.fields['skin_tone'].widget.attrs['class'] = "form-control"
        self.fields['skin_tone'].widget.attrs['placeholder'] = "choose your skin tone"
        self.fields['under_tone'].widget.attrs['class'] = "form-control"
        self.fields['under_tone'].widget.attrs['placeholder'] = "choose your under tone"
        self.fields['gender'].widget.attrs['class'] = "form-control"
        self.fields['gender'].widget.attrs['placeholder'] = "choose your gender"
        self.fields['picture'].widget.attrs['class'] = "form-control"
        self.fields['picture'].widget.attrs['placeholder'] = "choose your picture"
        self.fields['front_image'].widget.attrs['class'] = "form-control"
        self.fields['front_image'].widget.attrs['placeholder'] = "choose your front image"
        self.fields['back_image'].widget.attrs['class'] = "form-control"
        self.fields['back_image'].widget.attrs['placeholder'] = "choose your back image"


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'

    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
