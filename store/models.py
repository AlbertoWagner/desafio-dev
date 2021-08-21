from django.db import models


class Stores(models.Model):
    name = models.CharField(max_length=120)
    store_owner = models.CharField(max_length=120)

    class Meta:
        ordering = ['store_owner']
        verbose_name = u'Store'
        verbose_name_plural = u'Stores'
        db_table = 'stores'
