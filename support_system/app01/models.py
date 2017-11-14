from django.db import models

# Create your models here.

class Book(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=32)
    # author=models.CharField(max_length=32)
    publicDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)

    # 创建书与作者的多对多关系
    author=models.ManyToManyField("Author")

    #创建于书与出版社的一对多的关系
    publish=models.ForeignKey("Publish")

    def __str__(self):
        return self.title



class Loginuser(models.Model):
    id=models.AutoField(primary_key=True)
    sqlusername=models.CharField(max_length=32)
    sqlpassword=models.CharField(max_length=32)

class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()

    def __str__(self):
        return self.name


class Publish(models.Model):
    name=models.CharField(max_length=32)
    addr=models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Authordetal(models.Model):
    tel=models.IntegerField()
    addr=models.CharField(max_length=32)
    author = models.OneToOneField("Author")

