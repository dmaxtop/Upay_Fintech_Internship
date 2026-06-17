from django.db import models

class ActiveAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class SuccessfulTransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='SUCCESS')