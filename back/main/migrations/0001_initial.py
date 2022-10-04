# Generated by Django 4.0.4 on 2022-05-17 20:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', validators=[main.models.User.avatar_validator], verbose_name='Аватар')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Адрес электронной почты')),
                ('phone_number', models.CharField(blank=True, max_length=18, null=True, unique=True, verbose_name='Номер телефона')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('is_active', models.BooleanField(default=True, help_text='Отметьте, если пользователь должен считаться активным. Уберите эту отметку вместо удаления учётной записи.', verbose_name='Активный')),
                ('is_staff', models.BooleanField(default=False, help_text='Отметьте, если пользователь может входить в административную часть сайта.', verbose_name='Статус персонала')),
                ('is_superuser', models.BooleanField(default=False, help_text='Указывает, что пользователь имеет все права без явного их назначения.', verbose_name='Статус суперпользователя')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователя',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, unique=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название кафедры')),
            ],
            options={
                'verbose_name': 'Кафедру',
                'verbose_name_plural': 'Кафедры',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255, unique=True, verbose_name='Роль')),
                ('points', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)], verbose_name='Баллов')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=255, unique=True, verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('theme', models.ImageField(blank=True, null=True, upload_to='themes', verbose_name='Тема')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'verbose_name': 'Тему',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_code', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)], verbose_name='Шифр студента')),
                ('course', models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True, verbose_name='Курс')),
                ('rating', models.PositiveIntegerField(default=0, verbose_name='Рейтинг')),
                ('rating_study', models.PositiveIntegerField(default=0, verbose_name='Учёба')),
                ('rating_science', models.PositiveIntegerField(default=0, verbose_name='Наука')),
                ('rating_innovations', models.PositiveIntegerField(default=0, verbose_name='Инновации')),
                ('rating_culture', models.PositiveIntegerField(default=0, verbose_name='Культура')),
                ('rating_sport', models.PositiveIntegerField(default=0, verbose_name='Спорт')),
                ('rating_work', models.PositiveIntegerField(default=0, verbose_name='Работа')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.department', verbose_name='Кафедра')),
                ('speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.speciality', verbose_name='Специальность')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Студента',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Доцента',
                'verbose_name_plural': 'Доценты',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Рейтинг')),
                ('comment', models.TextField(blank=True, max_length=255, null=True, verbose_name='Комментарий')),
                ('points', models.PositiveIntegerField(default=0, verbose_name='Очков')),
                ('status', models.IntegerField(choices=[(-1, -1), (0, 0), (1, 1)], default=0, verbose_name='Статус')),
                ('date_sended', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата отправления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='events', validators=[main.models.Event.image_validator], verbose_name='Изображение')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('status', models.IntegerField(choices=[(-1, 'Закончено'), (1, 'Активно')], default=1, verbose_name='Статус')),
                ('date_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category', verbose_name='Категория')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.professor', verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.professor', verbose_name='Глава кафедры'),
        ),
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('value', models.CharField(max_length=255, unique=True, verbose_name='Значение')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'verbose_name': 'Кастомизацию',
                'verbose_name_plural': 'Кастомизация',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(-1, 'Отклонена'), (0, 'В ожидании'), (1, 'Одобрена')], default=0, verbose_name='Статус')),
                ('date_sended', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата отправления')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.event', verbose_name='Мероприятие')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student', verbose_name='Получатель')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.role', verbose_name='Роль')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Заявку',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]