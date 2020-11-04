from django.db import models
from django.contrib.auth.models import User
import datetime


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
    subject = models.CharField(max_length=30, verbose_name="科目")
    remark = models.CharField(max_length=500, verbose_name="备注", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ReleaseHomeWork", verbose_name="创建人")
    end_time = models.DateTimeField(verbose_name="截止时间", default=datetime.datetime.now())
    member_can_know_donelist = models.BooleanField(verbose_name="成员可查看完成情况", choices=((False, "否"), (True, "是")),
                                                   default=False)
    member_can_see_others = models.BooleanField(verbose_name="成员可互相查看作业", choices=((False, "否"), (True, "是")),
                                                default=False)


class DoneModel(models.Model):
    class Meta:
        db_table = "done"
        verbose_name = "作业完成情况"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.work

    work = models.ForeignKey(to=HomeWorkInfModel, verbose_name="作业", on_delete=models.CASCADE, related_name='done')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Done", verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 创建的时间
