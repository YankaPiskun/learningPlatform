from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class Subject(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование дисциплины')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Дисипилна'
        verbose_name_plural = 'Дисипилны'
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE,
                              verbose_name='Создатель курса')
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE,
                                verbose_name='Дисциплина')
    title = models.CharField(max_length=200, verbose_name='Название курса')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(verbose_name='Обзор на курс')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания курса')
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE,
                               verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название модуля')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module,
                related_name='contents', on_delete=models.CASCADE, verbose_name='Модуль')
    content_type = models.ForeignKey(ContentType,
                    on_delete=models.CASCADE, verbose_name='Тип контента',
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()



# Create your models here.
