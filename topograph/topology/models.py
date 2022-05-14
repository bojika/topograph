from random import randrange

from django.db import models
from django.urls import reverse_lazy

# Create your models here.


class Topology(models.Model):
    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('Finished', 'Finished'),
    )

    description = models.CharField(max_length=255, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(null=False, default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, blank=True)
    # owner = models.ForeignKey(User, related_name='begin', on_delete=models.CASCADE, null=False),
    # group = models.ManyToManyField('User')

    def get_absolute_url(self):
        return reverse_lazy('topology_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.description}'


class Node(models.Model):
    label = models.CharField(max_length=255)
    meta_data = models.JSONField(null=False, default=dict)
    x = models.FloatField(null=False, default=1)
    y = models.FloatField(null=False, default=1)
    topology = models.ForeignKey(Topology, on_delete=models.CASCADE, null=False)

    def get_absolute_url(self):
        return reverse_lazy('node_detail', kwargs={'pk': self.pk})

    #        return f"<{self.__class__.__name__} {self.label!r} {self.meta_data!r}>"
    def __str__(self):
        # return f'<{self.__class__.__name__} {self.label!r} {self.meta_data!r}>'
        return f'{self.label}'


class Edge(models.Model):
    begin = models.ForeignKey(Node, related_name='begin', on_delete=models.CASCADE, null=False)
    end = models.ForeignKey(Node, related_name='end', on_delete=models.CASCADE, null=False)
    cost = models.IntegerField(default=0)
    meta_data = models.JSONField(null=False, default=dict)

    def get_absolute_url(self):
        return reverse_lazy('edge_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.begin} <--> {self.end}'
        # return f"{self.__class__.__name__}: <<begin: {self.begin!r}, end: {self.end!r}, cost: {self.cost!r}, meta: {self.meta_data!r}>>"




