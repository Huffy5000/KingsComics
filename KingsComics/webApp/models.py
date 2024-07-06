from django.db import models

class Newsletter(models.Model):
    name = models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f'Name: {self.name}, Email: {self.email}'
