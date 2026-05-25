"""
Tenant model — client isolation for multi-tenant ESG data.

Every API request must include client_id (header X-Client-Id) so records
are scoped to a single enterprise client.
"""
from django.db import models


class Tenant(models.Model):
    """Enterprise client; all emissions data is scoped to one tenant."""

    client_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text='External client identifier used in API headers',
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.client_id})'
