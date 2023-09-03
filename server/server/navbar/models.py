from django.db import models

# Create your models here.
class Navbar(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Navbar"
        verbose_name_plural = "Navbar"
        ordering = ['order']