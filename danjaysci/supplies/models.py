from django.db import models
from django.contrib.auth.models import User
from institutions.models import Institution, Funding

# Create your models here.
class Vendor(models.Model):
    # A vendor is a person or company we purchase supplies from. They may or may not also manufacture their own products. At a minimum, we should have their name and a contact method, though coding below has allowed for no contact information to be input. This should be handled in validation.
    # Tufts has an e-procurement system, but all other billing systems should be supported.
    # Define list of billing methods
    MARKETPLACE = 1
    CREDIT_CARD = 2
    NET30 = 3
    E_PROCUREMENT = 4
    MAIL_INVOICE = 5
    BILLING_METHOD_OPTIONS = (
        (MARKETPLACE, 'Tufts Marketplace'),
        (CREDIT_CARD, 'Credit Card'),
        (NET30, 'Net 30'),
        (E_PROCUREMENT, 'Other E-Procurement'),
        (MAIL_INVOICE, 'Mailed invoice'),
    )

    name = models.CharField(max_length = 128)
    contact_person = models.CharField(
        max_length = 128,
        blank = True,
        null = True,
    )
    contact_title = models.CharField(
        max_length = 128,
        blank = True,
        null = True,
    )
    contact_email = models.EmailField(
        blank = True,
        null = True,
    )
    contact_phone = models.CharField(
        max_length = 32,
        blank = True,
        null = True,
    )
    billing_method = models.IntegerField(
        choices = BILLING_METHOD_OPTIONS,
    )
    website = models.URLField(
        blank = True,
        null = True,
    )
    notes = models.TextField(blank = True)

    def __str__(self):
        return '%s' % self.name
    
    class Meta:
        ordering = ['name']

class WebAccount(models.Model):
    # Keep a list of website logins for vendors not on the Tufts Marketplace
    vendor = models.ForeignKey(
        Vendor,
        on_delete = models.PROTECT,
    )
    username = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)
    associated_email = models.EmailField()
    website = models.CharField(
        max_length = 128,
        blank = True,
    )

    def __str__(self):
        return '%s: %s' % (self.vendor, self.username)

    class Meta:
        ordering = ['vendor']

class SupplyCategory(models.Model):
    # Keep track of supply cetegories, and flag those that have special inventory requirements, e.g. chemicals, radioactive materials, antibodies, etc.
    name = models.CharField(max_length = 64)
    special_inventory_required = models.BooleanField(default = False)
    notes = models.TextField(blank = True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name_plural = "Supply categories"
        ordering = ['name']

class Item(models.Model):
    # Keep track of items separately from their prices, as prices change over time
    category = models.ManyToManyField(SupplyCategory)

    name = models.CharField(max_length = 64)
    manufacturer = models.CharField(
        max_length = 64,
        help_text = "The brand or name of the company that makes this item, not who we bought it from. For example, we frequently buy Corning-branded 10-cm tissue culture dishes from Fisher Scientific, so the manufacturer here is Corning, and the vendor is Fisher Scientific. In another case, we buy Abcam antibodies directly from Abcam, so the manufacturer and vendor are both Abcam.",
    )
    catalog_number = models.CharField(max_length = 32)
    description = models.CharField(max_length = 128)

    def __str__(self):
        return '%s (%s #%s)' % (self.name, self.manufacturer, self.catalog_number)

    class Meta:
        ordering = ['name', 'manufacturer']

class Quote(models.Model):
    # Keep track of quotes from vendors, which may have a different contact person than the normal vendor contact. A quote can have multiple items and item costs, so track this.
    vendor = models.ForeignKey(
        Vendor,
        on_delete = models.PROTECT,
    )

    items = models.ManyToManyField(Item)

    number = models.CharField(max_length = 32)
    valid_from = models.DateField()
    valid_until = models.DateField()
    contact_person = models.CharField(max_length = 128)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length = 32)

    def __str__(self):
        return 'Quote #%s, %s' % (self.number, self.vendor)

    class Meta:
        ordering = ['-valid_until', 'vendor']

class ItemPrice(models.Model):
    # The price of an item can change over time, so keep track of spot pricing and which vendor gives a particular price. This particular price may or may not be associated with a specific quote, so allow for that. Some quotes also specify a minimum order quantity.
    item = models.ForeignKey(
        Item,
        on_delete = models.PROTECT,
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete = models.PROTECT,
    )

    quote = models.ForeignKey(
        Quote,
        on_delete = models.PROTECT,
        blank = True,
        null = True,
    )

    vendor_catalog_number = models.CharField(max_length = 32)
    quantity = models.PositiveSmallIntegerField()
    quantity_unit = models.CharField(max_length = 32)
    min_quantity_req = models.PositiveSmallIntegerField(
        verbose_name = "minimum quantity required for quoted price",
        blank = True,
        null = True,
    )
    unit_cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 8,
    )
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return '%s @ $%s / %s (%s #%s)' % (self.item, self.unit_cost, self.quantity_unit, self.vendor, self.vendor_catalog_number)

    class Meta:
        ordering = ['item', '-date']

class Order(models.Model):
    # Keep track of orders.
    # Orer methods
    MARKETPLACE = 1
    WEBSITE = 2
    OTHER = 3
    ORDER_METHODS_OPTIONS = (
        (MARKETPLACE, 'Tufts Marketplace'),
        (WEBSITE, 'Website'),
        (OTHER, 'Other'),
    )

    placed_by = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
        related_name = 'placed_orders',
    )

    received_by = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
        blank = True,
        null = True,
        related_name = 'received_orders'
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete = models.PROTECT,
    )

    charge_to = models.ForeignKey(
        Funding,
        on_delete = models.PROTECT,
    )
    
    order_method = models.IntegerField(
        choices = ORDER_METHODS_OPTIONS,
    )
    order_number = models.CharField(
        max_length = 32,
        blank = True,
    )
    invoice_number = models.CharField(
        max_length = 32,
        blank = True,
    )
    shipping_cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 8,
        blank = True,
        default = 0.00
    )
    date_ordered = models.DateField()
    date_received = models.DateField(
        blank = True,
        null = True,
    )

    def __str__(self):
        return 'Order #%s, %s (%s)' % (self.order_number, self.vendor, self.placed_by)

    class Meta:
        ordering = ['-date_ordered']

class LineItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete = models.PROTECT,
    )

    item_price = models.ForeignKey(
        ItemPrice,
        on_delete = models.PROTECT,
    )

    quantity_ordered = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s %s @ %s' % (self.item_price.item, self.quantity_ordered, self.item_price)

    class Meta:
        ordering = ['order']

class ItemRequest(models.Model):
    # Define priority list
    URGENT_PRIORITY = 0
    HIGH_PRIORITY = 1
    MEDIUM_PRIORITY = 2
    LOW_PRIORITY = 3
    WISHLIST_PRIORITY = 9
    PRIORITY_CHOICES = (
        (URGENT_PRIORITY, 'Urgent! (Needed it yesterday)'),
        (HIGH_PRIORITY, 'High (Need it ASAP)'),
        (MEDIUM_PRIORITY, 'Medium (Need with within a week'),
        (LOW_PRIORITY, 'Low (Need it sometime soon)'),
        (WISHLIST_PRIORITY, 'Wishlist (Thinking about it)'),
    )

    item = models.ForeignKey(
        Item,
        on_delete = models.PROTECT,
        blank = True
    )

    requested_by = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
        related_name = 'requested_orders',
    )

    date_requested = models.DateField(auto_now_add = True)
    quantity = models.PositiveSmallIntegerField()
    quantity_unit = models.CharField(max_length = 16)
    unit_cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 8,
    )
    priority = models.IntegerField(
        choices = PRIORITY_CHOICES,
        default = MEDIUM_PRIORITY,
    )
    suggested_vendor = models.CharField(
        max_length = 32,
        blank = True,
    )
    intended_use = models.TextField()
    substitutions_allowed = models.BooleanField(default = True)
    
    # Resrict access to the following fields to users who have ordering privileges
    ordered_by = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
        blank = True,
        null = True,
        related_name = 'fulfilled_requests',
    )
    order_line_item = models.OneToOneField(
        LineItem,
        on_delete = models.PROTECT,
        blank = True,
        null = True,
        related_name = "fulfilling_request",
    )
    denied = models.BooleanField(default = False)

    def __str__(self):
        return '%s: %s %s %s; %s' % (self.requested_by, self.quantity, self.quantity_unit, self.item, PRIORITY_CHOICES[self.priority])

    class Meta:
        ordering = ['-denied', 'priority', 'date_requested']
