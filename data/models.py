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
        return f"{self.text} - {self.label}"


class Train(models.Model):
    task_id = models.CharField(verbose_name="Task id", max_length=254)
    user = models.ForeignKey(
        verbose_name="User", to="auth.User", related_name="train", null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True, editable=False)

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trains"

    def __str__(self):
        return f"{self.task_id}"
