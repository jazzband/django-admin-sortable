from django.db import models

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable


class SimpleModel(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


#a model that is sortable
class Category(SimpleModel, Sortable):
    class Meta(Sortable.Meta):
        """
        Classes that inherit from Sortable must define an inner
        Meta class that inherits from Sortable.Meta or ordering
        won't work as expected
        """
        verbose_name_plural = 'Categories'


#a model that is sortable relative to a foreign key that is also sortable
#uses SortableForeignKey field. Works with versions 1.3+
class Project(SimpleModel, Sortable):
    class Meta(Sortable.Meta):
        pass

    category = SortableForeignKey(Category)
    description = models.TextField()


#registered as a tabular inline on `Project`
class Credit(Sortable):
    class Meta(Sortable.Meta):
        pass

    project = models.ForeignKey(Project)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


#registered as a stacked inline on `Project`
class Note(Sortable):
    class Meta(Sortable.Meta):
        pass

    project = models.ForeignKey(Project)
    text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text
