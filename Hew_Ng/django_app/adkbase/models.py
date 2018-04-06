# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Gene(models.Model):
    entrez_id = models.IntegerField(default=0) 
    gene_symbol =  models.CharField(max_length=10)
    gene_name =  models.CharField(max_length=200)
    def __str__(self):
        return u'entrez_id: %s \nGene Symbol: %s \nGene Name: %s' % (self.entrez_id, self.gene_symbol, self.gene_name)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
