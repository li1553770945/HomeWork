from django.db import models
from django.contrib.auth.models import User
from work.models import HomeWorkInfModel


# Create your models here.
class GroupModel(models.Model):
    class Meta:
        db_table = "user_group"
        verbose_name = "分组"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=30, verbose_name="组名", db_index=True)
    desc = models.TextField('描述', default='', blank=True, null=True, max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人', related_name="own_groups",
                              db_index=True)
    password = models.CharField(max_length=20, verbose_name="小组密码", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_members(self):
        yield self.owner
        join_groups = GroupMembersModel.objects.filter(group=self)
        for member in join_groups:
            yield member.user


class GroupMembersModel(models.Model):
    class Meta:
        db_table = "group_members"
        verbose_name = "小组成员"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", related_name="joined_groups",
                             db_index=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, verbose_name="小组", related_name="members")
    time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")

    def __str__(self):
        return "{}-{}".format(self.group,self.user.first_name)


class WorkGroupModel(models.Model):
    class Meta:
        db_table = "homeworkgroup"
        verbose_name = "作业小组"
        verbose_name_plural = verbose_name

    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, verbose_name="小组", related_name="work")
    work = models.ForeignKey(HomeWorkInfModel, on_delete=models.CASCADE, verbose_name="作业", related_name="groups")
