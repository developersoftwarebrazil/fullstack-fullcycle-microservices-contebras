# Generated by Django 5.1.2 on 2024-11-04 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleCourse', models.CharField(max_length=255, verbose_name='Título do curso')),
                ('description', models.TextField(verbose_name='Descrição do curso')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Nome padrão', max_length=100, verbose_name='Nome')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='contebras_core.course')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('studentEmail', models.EmailField(max_length=100, verbose_name='Email do aluno')),
                ('classroom', models.ManyToManyField(related_name='student', to='contebras_core.classroom', verbose_name='Turma')),
                ('curse', models.ManyToManyField(related_name='student', to='contebras_core.course', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
            },
        ),
        migrations.CreateModel(
            name='RegistrationClassroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contebras_core.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contebras_core.student')),
            ],
            options={
                'verbose_name': 'Matrícula',
                'verbose_name_plural': 'Matrículas',
            },
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(related_name='classrooms', through='contebras_core.RegistrationClassroom', to='contebras_core.student'),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('thumbnail', models.ImageField(upload_to='thumbnails/', verbose_name='Miniaturas')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('published_at', models.DateTimeField(editable=False, null=True, verbose_name='Publicado em')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publicado')),
                ('num_likes', models.IntegerField(default=0, editable=False, verbose_name='número de curtidas')),
                ('num_viewa', models.IntegerField(default=0, editable=False, verbose_name='número de vidualizações')),
                ('tags', models.ManyToManyField(related_name='videos', to='contebras_core.tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Vídeo',
                'verbose_name_plural': 'Vídeos',
            },
        ),
        migrations.CreateModel(
            name='VideoMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_path', models.CharField(max_length=255, verbose_name='Vídeo')),
                ('status', models.CharField(choices=[('UPLOADED_STARTED', 'Upload Iniciado'), ('PROCESSING_STARTED', 'Processamento Iniciado'), ('PROCESSING_FINISHED', 'Processamento Finalizado'), ('PROCESSING_ERROR', 'Erro no Processamento')], default='UPLOADED_STARTED', max_length=20, verbose_name='Status')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='video_media', to='contebras_core.video', verbose_name='Vídeo')),
            ],
        ),
    ]