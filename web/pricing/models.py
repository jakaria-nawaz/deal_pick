from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BaseModelTitle(BaseModel):
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Currency(BaseModelTitle):
    pass


class Country(BaseModelTitle):
    pass


class Shop(BaseModelTitle):
    url = models.URLField()
    currency = models.ForeignKey(Currency, null=True, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)


class Product(BaseModelTitle):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)


class Price(BaseModel):
    price = models.FloatField()
    currency = models.ForeignKey(Currency, null=True, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
