from django.db import models
from django.contrib.auth.models import User


risks = [
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low')
]

days = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday')
]


results = [
    ('Success', 'Success'),
    ('Failed', 'Failed')
]



class Trade(models.Model):
    currency = models.CharField(max_length=20, blank=True, null=True, default="Gold")
    total_money = models.DecimalField(max_digits=15, decimal_places=2)
    lot = models.DecimalField(max_digits=15, decimal_places=2)
    profit_or_loss = models.DecimalField(max_digits=15, decimal_places=2)
    time_on_chart  = models.IntegerField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    risk = models.CharField(max_length=20, choices=risks, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    day = models.CharField(max_length=20, choices=days)
    result = models.CharField(max_length=20, choices=results)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.currency