from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class HomeWorkInfModel(models.Model):
    class Meta:
        db_table = "homeworkinformation"
        verbose_name = "作业信息"
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=50,verbose_name="作业名称")  # 作业的名字
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")  # 创建的时间
    subject = models.CharField(max_length=30,verbose_name="科目")
    remark = models.CharField(max_length=500,verbose_name="备注",null=True,blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ReleaseHomeWork",verbose_name="创建人")
