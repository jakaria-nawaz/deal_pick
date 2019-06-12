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

    def __str__(self):
        return self.title


class Country(BaseModelTitle):
    pass

    def __str__(self):
        return self.title


class Shop(BaseModelTitle):
    url = models.URLField()
    currency = models.ForeignKey(Currency, null=True, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Product(BaseModelTitle):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    image = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = (('title', 'shop'),)

    def __str__(self):
        return self.title


class Price(BaseModel):
    price = models.FloatField()
    currency = models.ForeignKey(Currency, null=True, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    url = models.URLField(null=True)

    def __str__(self):
        return self.product.title


class SearchQuery(BaseModelTitle):
    product = models.ManyToManyField(Product)

