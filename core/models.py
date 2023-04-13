from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

TOP = 'top_piece'
BOTTOM = 'bottom_piece'
ONEPIECE = 'one_piece'
OTHER = 'other'
WEARING_PART_CHOICES = (
    (TOP, 'Top Piece'),
    (BOTTOM, 'Bottom Piece'),
    (ONEPIECE, 'One Piece'),
    (OTHER, 'Other'),
)

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
SKIN_TONE_CHOICES = (
        ('F', 'Fair'),
        ('M', 'Medium'),
        ('D', 'Dark'),
)
UNDER_TONE_CHOICES = (
        ('W', 'Warm'),
        ('C', 'Cool'),
        ('N', 'Neutral'),
    )
class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })


class BodyType(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Occasion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Weather(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class DressType(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Measurements(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Gender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Item(models.Model):
    OCCASION_CHOICES = (
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('semi_formal', 'Semi-Formal'),
        ('business_or_professional', 'Business/Professional'),
        ('romantic_date', 'Romantic Date'),
        ('sports_athletic', 'Sports/Athletic'),
        ('sport', 'Sport'),
        ('party', 'Party'),
    )
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    title = models.CharField(max_length=100)
    # type = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(DressType, on_delete=models.CASCADE,blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    occasion = models.ManyToManyField(Occasion)
    weather = models.ManyToManyField(Weather)
    # gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=MALE)
    gender = models.ManyToManyField(Gender, blank=True)
    color_description = models.CharField(max_length=100, blank=True, null=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)
    matching_outfit = models.ManyToManyField("self", blank=True)
    Measurements = models.ManyToManyField(Measurements, blank=True)
    # weather = models.CharField(max_length=100,choices=WEATHER_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    wearing_part = models.CharField(max_length=20, choices=WEARING_PART_CHOICES, default=OTHER)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    body_type = models.ManyToManyField(BodyType,blank=True)
    slug = models.SlugField()
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField()
    vton_image = models.ImageField(blank=True,null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):

        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    high_hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skin_tone = models.CharField(max_length=1, choices=SKIN_TONE_CHOICES, null=True, blank=True)
    under_tone = models.CharField(max_length=1, choices=UNDER_TONE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    picture = models.ImageField(upload_to='user',blank=True)
    front_image = models.ImageField(upload_to='user/front',blank=True)
    back_image = models.ImageField(upload_to='user/back',blank=True)
    def __str__(self):
        return self.user.username
