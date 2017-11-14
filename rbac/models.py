from django.db import models

# Create your models here.
"""
用户的权限设置在url中，表里可以存放所有的url
根据角色来分配权限
"""

class Permission(models.Model):
    """
    权限表
    verbose_name:(?)
    class Meta:(?)
        verbose_name_plural="权限表"
    """
    title=models.CharField(verbose_name='标题',max_length=32)
    url=models.CharField(verbose_name='含有正则的url',max_length=32)

    is_menu=models.BooleanField(verbose_name='是否做菜单')

    class Meta:
        verbose_name_plural="权限表"

    def __str__(self):
        return self.title



class User(models.Model):
    """
    用户表
    """
    username=models.CharField(verbose_name='用户名',max_length=32)
    password=models.CharField(verbose_name='密码',max_length=32)
    email=models.CharField(verbose_name='邮箱',max_length=32)

    roles=models.ManyToManyField(verbose_name='具有的角色',to="Role")

    class Meta:
        verbose_name_plural="用户表"

    def __str__(self):
        return self.username

class Role(models.Model):
    """
    角色表
    """
    title=models.CharField(verbose_name='角色名称',max_length=32)
    permission=models.ManyToManyField(to="Permission")

    class Meta:
        verbose_name_plural="角色表"

    def __str__(self):
        return self.title

