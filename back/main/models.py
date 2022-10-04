from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import UserManager




class User(AbstractBaseUser, PermissionsMixin):    
    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


    def avatar_validator(avatar):
        max_width = 256
        max_height = max_width


        if avatar.width > max_width or avatar.height > max_height:
            raise ValidationError(_(f'Высота/Ширина > {max_width}px'))


    avatar = models.ImageField(verbose_name=_('Аватар'), upload_to='avatars', validators=[avatar_validator], blank=True, null=True)

    username = models.CharField(verbose_name=_('Имя пользователя'), max_length=255, unique=True)    
    email = models.EmailField(verbose_name=_('Адрес электронной почты'), unique=True, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('Номер телефона'), max_length=18, unique=True, blank=True, null=True)

    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=255, blank=True, null=True)
    first_name = models.CharField(verbose_name=_('Имя'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(verbose_name=_('Отчество'), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(verbose_name=_('Активный'), help_text=_('Отметьте, если пользователь должен считаться активным. Уберите эту отметку вместо удаления учётной записи.'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Статус персонала'), help_text=_('Отметьте, если пользователь может входить в административную часть сайта.'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Статус суперпользователя'), help_text=_('Указывает, что пользователь имеет все права без явного их назначения.'), default=False)

    date_joined = models.DateTimeField(verbose_name=_('Дата регистрации'), default=timezone.now)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    objects = UserManager()


    def __str__(self):
        return self.username

class Professor(models.Model):
    class Meta:
        verbose_name = 'Доцента'
        verbose_name_plural = 'Доценты'


    user = models.OneToOneField(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

class Category(models.Model):    
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


    category = models.CharField(verbose_name=_('Категория'), max_length=255, unique=True)

    
    def __str__(self):
        return self.category

class Role(models.Model):    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


    role = models.CharField(verbose_name=_('Роль'), max_length=255, unique=True)

    points = models.PositiveIntegerField(verbose_name=_('Баллов'), validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0)

    
    def __str__(self):
        return self.role

class Department(models.Model):
    class Meta:
        verbose_name = 'Кафедру'
        verbose_name_plural = 'Кафедры'


    name = models.CharField(verbose_name=_('Название кафедры'), max_length=255, unique=True)
    
    head = models.ForeignKey(Professor, verbose_name=_('Глава кафедры'), on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Speciality(models.Model):
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


    speciality = models.CharField(verbose_name=_('Специальность'), max_length=255, unique=True)

    department = models.ForeignKey(Department, verbose_name=_('Кафедра'), on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.speciality

class Student(models.Model):
    class Meta:
        verbose_name = 'Студента'
        verbose_name_plural = 'Студенты'

    
    COURSE = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]


    user = models.OneToOneField(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    student_code = models.PositiveIntegerField(verbose_name=_('Шифр студента'), validators=[MinValueValidator(10000), MaxValueValidator(99999)], unique=True, blank=True, null=True)

    # department = models.ForeignKey(Department, verbose_name=_('Кафедра'), on_delete=models.SET_NULL, blank=True, null=True)

    speciality = models.ForeignKey(Speciality, verbose_name=_('Специальность'), on_delete=models.SET_NULL, blank=True, null=True)
    course = models.PositiveIntegerField(verbose_name=_('Курс'), choices=COURSE, blank=True, null=True)

    rating = models.PositiveIntegerField(verbose_name=_('Рейтинг'), default=0)
    rating_study = models.PositiveIntegerField(verbose_name=_('Учёба'), default=0)
    rating_science = models.PositiveIntegerField(verbose_name=_('Наука'), default=0)
    rating_innovations = models.PositiveIntegerField(verbose_name=_('Инновации'), default=0)
    rating_culture = models.PositiveIntegerField(verbose_name=_('Культура'), default=0)
    rating_sport = models.PositiveIntegerField(verbose_name=_('Спорт'), default=0)
    rating_work = models.PositiveIntegerField(verbose_name=_('Работа'), default=0)


    def __str__(self):
        return str(self.student_code)

    def save(self, *args, **kwargs):
        sum_rating_study = 0
        sum_rating_science = 0
        sum_rating_innovations = 0
        sum_rating_culture = 0
        sum_rating_sport = 0
        sum_rating_work = 0

        applications = Application.objects.all()

        for i in applications:
            if self == i.recipient:
                if i.status == 1:
                    match str(i.event.category):
                        case 'Учёба':
                            sum_rating_study += i.role.points
                        case 'Наука':
                            sum_rating_science += i.role.points
                        case 'Инновации':
                            sum_rating_innovations += i.role.points
                        case 'Культура':
                            sum_rating_culture += i.role.points
                        case 'Спорт':
                            sum_rating_sport += i.role.points
                        case 'Работа':
                            sum_rating_work += i.role.points
                        case _:
                            pass
        
        
        self.rating_study = sum_rating_study
        self.rating_science = sum_rating_science
        self.rating_innovations = sum_rating_innovations
        self.rating_culture = sum_rating_culture
        self.rating_sport = sum_rating_sport
        self.rating_work = sum_rating_work

        self.rating = self.rating_study + self.rating_science + self.rating_innovations + self.rating_culture + self.rating_sport + self.rating_work


        super(Student, self).save(*args, **kwargs)


class Event(models.Model):
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


    def image_validator(image):
        max_width = 1920
        max_height = 1080


        if image.width > max_width or image.height > max_height:
            raise ValidationError(_(f'Ширина > {max_width}px/Высота > {max_height}px'))


    STATUS = [
        (-1, 'Закончено'),
        (1, 'Активно'),
    ]


    image = models.ImageField(verbose_name=_('Изображение'), upload_to='events', validators=[image_validator], blank=True, null=True)

    creator = models.ForeignKey(Professor, verbose_name=_('Создатель'), on_delete=models.CASCADE)   

    name = models.CharField(verbose_name=_('Название'), max_length=255, unique=True)

    category = models.ForeignKey(Category, verbose_name=_('Категория'), blank=True, null=True, on_delete=models.SET_NULL)

    status = models.IntegerField(verbose_name=_('Статус'), choices=STATUS, default=1)

    date_start = models.DateTimeField(verbose_name=_('Дата начала'), default=timezone.now)
    date_end = models.DateTimeField(verbose_name=_('Дата окончания'), blank=True, null=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if self.date_start <= timezone.now() <= self.date_end:
        #     self.status = 1
        # else:
        #     self.status = -1
        print(self.date_start)
        print(timezone.now())

        super(Event, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print('delete one / event')
        for i in self.application_set.all():
            i.delete()
        
        super(Event, self).delete(*args, **kwargs)

class Application(models.Model):
    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

    
    STATUS = [
        (-1, 'Отклонена'),
        (0, 'В ожидании'),
        (1, 'Одобрена'),
    ]


    event = models.ForeignKey(Event, verbose_name=_('Мероприятие'), on_delete=models.CASCADE)

    sender = models.ForeignKey(User, related_name='sender', verbose_name=_('Отправитель'), on_delete=models.CASCADE)
    recipient = models.ForeignKey(Student, verbose_name=_('Получатель'), on_delete=models.CASCADE)

    role = models.ForeignKey(Role, verbose_name=_('Роль'), on_delete=models.SET_NULL, blank=True, null=True)

    status = models.IntegerField(verbose_name=_('Статус'), choices=STATUS, default=0)

    date_sended = models.DateTimeField(verbose_name=_('Дата отправления'), default=timezone.now)


    def __str__(self):
        return self.event.name

    def save(self, *args, **kwargs):
        super(Application, self).save(*args, **kwargs)

        self.recipient.save()

    def delete(self, *args, **kwargs):
        print('delete one / application (models.py)')
        super(Application, self).delete(*args, **kwargs)

        self.recipient.save()

    # def delete_queryset(self, *args, **kwargs):
    #     print('delete query set / application')
    #     super(Application, self).delete(*args, **kwargs)

    #     self.recipient.save()

class Theme(models.Model):
    class Meta:
        verbose_name = 'Тему'
        verbose_name_plural = 'Темы'


    name = models.CharField(verbose_name=_('Название'), max_length=255, unique=True)

    theme = models.ImageField(verbose_name=_('Тема'), upload_to='themes', blank=True, null=True)

    users = models.ManyToManyField(User, verbose_name=_('Пользователи'))


    def __str__(self):
        return self.name

class Customization(models.Model):
    class Meta:
        verbose_name = 'Кастомизацию'
        verbose_name_plural = 'Кастомизация'


    name = models.CharField(verbose_name=_('Название'), max_length=255, unique=True)
    value = models.CharField(verbose_name=_('Значение'), max_length=255, unique=True)

    users = models.ManyToManyField(User, verbose_name=_('Пользователи'))


    def __str__(self):
        return self.name

class Feedback(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


    RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    STATUS = [
        (-1, -1),
        (0, 0),
        (1, 1),
    ]


    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(verbose_name=_('Рейтинг'), choices=RATING)
    comment = models.TextField(verbose_name=_('Комментарий'), max_length=255, blank=True, null=True)

    points = models.PositiveIntegerField(verbose_name=_('Очков'), default=0)

    status = models.IntegerField(verbose_name=_('Статус'), choices=STATUS, default=0)

    date_sended = models.DateTimeField(verbose_name=_('Дата отправления'), default=timezone.now)


    def __str__(self):
        return str(self.user)
