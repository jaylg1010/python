from django.db import models

# Create your models here.

class UserInfo(models.Model):
    """
    员工表
    """
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=64,verbose_name="密码")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="用户表"


class ClassList(models.Model):
    """
    班级表
    """
    title=models.CharField(max_length=32,verbose_name="班级表")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="班级表"


class Student(models.Model):
    """
    学生表
    """
    username=models.CharField(max_length=32,verbose_name="学生名")
    password=models.CharField(max_length=64,verbose_name="密码")
    cla=models.ForeignKey(to=ClassList,verbose_name="学生所属班级")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="学生表"


class Questionnaire(models.Model):
    """
    问卷表
    """
    title=models.CharField(max_length=32,verbose_name="问卷名")
    cla=models.ForeignKey(to="ClassList",verbose_name="班级关联的问卷")
    creator=models.ForeignKey(to="UserInfo",verbose_name="问卷的创建者")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="问卷表"


class Question(models.Model):
    """
    问题表
    """
    caption=models.CharField(max_length=64,verbose_name="问题名")

    question_type=(
        (1,"打分"),
        (2,"单选"),
        (3,"评价"),
    )

    type=models.IntegerField(choices=question_type,verbose_name="问题类型")
    questionnaire=models.ForeignKey(to=Questionnaire,verbose_name="问题所对应的问卷")

    def __str__(self):
        return self.caption


class Option(models.Model):
    """
    单选题的选项
    """
    name=models.CharField(verbose_name='单选的名称',max_length=32)
    score=models.IntegerField(verbose_name="选项对应的分数")

    question=models.ForeignKey(to=Question,verbose_name="单选对应的问题")

    def __str__(self):
        return self.name


class Answer(models.Model):
    """
    答案表
    """
    student=models.ForeignKey(to=Student,verbose_name="答案对应的学生")
    question=models.ForeignKey(to=Question,verbose_name="答案对应的问题")

    option=models.ForeignKey(to=Option,null=True,blank=True)
    val=models.IntegerField(null=True,blank=True)
    content=models.CharField(max_length=255,null=True,blank=True)