from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import m2m_changed, pre_save
import logging

logger = logging.getLogger(__name__)


# Create your models here.
class HomeWorkInfModel(models.Model):
    class Meta:
        db_table = "homeworkinformation"
        verbose_name = "作业信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, verbose_name="作业名称")  # 作业的名字
    type = models.CharField(max_length=100, choices=(('file', "文件"), ('hypertext', "超文本")), default="hypertext",
                            verbose_name="作业类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 创建的时间
    subject = models.CharField(max_length=30, verbose_name="科目",db_index=True)
    remark = models.CharField(max_length=500, verbose_name="备注", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ReleaseHomeWork", verbose_name="创建人",db_index=True)
    end_time = models.DateTimeField(verbose_name="截止时间", default=datetime.datetime.now())
    member_can_know_donelist = models.BooleanField(verbose_name="成员可查看完成情况", choices=((False, "否"), (True, "是")),
                                                   default=False)
    member_can_see_others = models.BooleanField(verbose_name="成员可互相查看作业", choices=((False, "否"), (True, "是")),
                                                default=False)
    groups = models.ManyToManyField(to='group.GroupModel', related_name="work", verbose_name="参与组")

    members = models.ManyToManyField(to=User, related_name='work', verbose_name='参与人员', through='HomeWorkMembersModel')

    can_submit_after_end = models.BooleanField(default=True,verbose_name="截止时间已过仍然可以提交")

class HomeWorkMembersModel(models.Model):
    class Meta:
        db_table = "done"
        verbose_name = "作业完成情况"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.work, self.owner)

    work = models.ForeignKey(to=HomeWorkInfModel, verbose_name="作业", on_delete=models.CASCADE, related_name='done',db_index=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Done", verbose_name="参与人",db_index=True)

    done = models.BooleanField(verbose_name="已完成", db_index=True, default=False)
    end_time = models.DateTimeField(verbose_name="截止时间")  # 创建的时间
    upload_time = models.DateTimeField(verbose_name="提交时间",null=True)
    file_name = models.CharField(max_length=100,verbose_name="保存文件名",default="")


def create_homework_members(sender, instance, **kwargs):
    for group in instance.groups.all():
        for member in group.get_members():
            HomeWorkMembersModel.objects.update_or_create(defaults={'end_time': instance.end_time}, work=instance,
                                                          owner=member)


def change_end_time(sender, instance, **kwargs):
    HomeWorkMembersModel.objects.filter(work=instance).update(end_time=instance.end_time)


m2m_changed.connect(create_homework_members, sender=HomeWorkInfModel.groups.through)
pre_save.connect(change_end_time, sender=HomeWorkInfModel)
