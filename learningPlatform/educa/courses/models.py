from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title



# Create your models here.
