# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 08:48
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('avatar', models.FileField(default='/avatar/default.png', upload_to='avatar/', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('desc', models.CharField(max_length=255, verbose_name='文章描述')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article_type_id', models.IntegerField(choices=[(1, '编程语言'), (2, '软件设计'), (3, '前端'), (4, '操作系统'), (5, '数据库')], default=None)),
            ],
            options={
                'verbose_name_plural': '文章表',
            },
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='文章')),
            ],
            options={
                'verbose_name_plural': '文章对应的标签表',
            },
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='所属文章')),
            ],
            options={
                'verbose_name_plural': '文章详细表',
            },
        ),
        migrations.CreateModel(
            name='ArticleUp',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '文章点赞表',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, unique=True, verbose_name='个人博客后缀')),
                ('theme', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '站点信息',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': '博客个人文章分类表',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('up_count', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='评论文章')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment', verbose_name='父级评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
            ],
            options={
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='CommentUp',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '评论点赞表',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='标签名称')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Category', verbose_name='文章类型'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='app01.Article2Tag', to='app01.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
