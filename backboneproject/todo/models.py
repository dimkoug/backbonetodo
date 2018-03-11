from django.db import models

# Create your models here.


class Todo(models.Model):
    owner = models.ForeignKey('auth.User', related_name='todos',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('-created',)
