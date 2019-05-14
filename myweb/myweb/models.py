# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.


class Task(models.Model):
    '''
    任务信息
    '''
    id = models.AutoField(primary_key=True)
    TaskID = models.CharField(max_length=125,verbose_name='任务ID')
    Taskname = models.CharField(max_length=125, verbose_name='任务名称')
    Starttime = models.DateTimeField(default=timezone.now, verbose_name='开始时间')
    Taksstatus = models.CharField(max_length=125, verbose_name='任务状态')
    Completiontime = models.CharField(max_length=125,blank=True,null=True, verbose_name='结束时间')
    Cmdb = models.ForeignKey('Cmdb', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = verbose_name
        ordering = ['Starttime']

    def __unicode__(self):
        return self.Taskname


class Cmdb(models.Model):
    '''
    资产信息
    '''
    id = models.AutoField(primary_key=True)
    Sn = models.CharField(max_length=125, verbose_name='sn')
    Hostname = models.CharField(max_length=125, verbose_name='主机名')
    OsVersion = models.CharField(max_length=125, verbose_name='操作系统版本')
    Ip = models.CharField(max_length=125, verbose_name='ip')
    Netmask = models.CharField(max_length=125, verbose_name='子网掩码')
    GW = models.CharField(max_length=125, verbose_name='网关')
    Mac = models.CharField(max_length=125, verbose_name='mac地址')
    iLoIp = models.CharField(max_length=125, verbose_name='带外ip')
    iLoNetmask = models.CharField(max_length=125, verbose_name='带外子网掩码')
    iLoGW = models.CharField(max_length=125, verbose_name='带外网关')
    iLoMac = models.CharField(max_length=125, verbose_name='带外mac')

    class Meta:
        verbose_name = 'Cmdb'
        verbose_name_plural = verbose_name
        ordering = ['Ip']

    def __unicode__(self):
        return self.Sn


class TaskInfo(models.Model):
    '''
    任务进度
    '''
    #id = models.IntegerField(primary_key=True) 
    id = models.AutoField(primary_key=True)
    TaskDetail = models.CharField(max_length=200,blank=True,null=True,verbose_name='任务详情')
    Task = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TaskInfo'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.TaskDetail
