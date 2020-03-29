from django.conf import settings
from django.db import models


class Data(models.Model):
    label = models.TextField(verbose_name="Label")
    text = models.TextField(verbose_name="Text")
    creator = models.ForeignKey(
        verbose_name="Creator", to="auth.User", related_name="data", null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True, editable=False)

    class Meta:
        verbose_name = "Data"
        verbose_name_plural = "Data"
        unique_together = (("text", "label"),)

    def __str__(self):
        return "{text} - {label}".format(text=self.text, label=self.label)
