from django.db import models

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
class Project(SimpleModel, Sortable):
    class Meta(Sortable.Meta):
        pass

#    @classmethod
#    def sortable_by(cls):
#        return Category, 'category'

    category = models.ForeignKey(Category)
    description = models.TextField()

    sortable_by = Category


#a model that is sortable relative to a foreign key that is also sortable
class Sample(SimpleModel, Sortable):
    class Meta(Sortable.Meta):
        pass

    category = models.ForeignKey(Category)
    description = models.TextField()

    #field to define which foreign key the model is sortable by.
    #works with versions > 1.1.1
    sortable_by = Category


#registered as a tabular inline on project
class Credit(Sortable):
    class Meta(Sortable.Meta):
        pass

    project = models.ForeignKey(Project)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


#registered as a stacked inline on project
class Note(Sortable):
    class Meta(Sortable.Meta):
        pass

    project = models.ForeignKey(Project)
    text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text
