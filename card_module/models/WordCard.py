from django.contrib.auth.models import User
from django.db import models


class WordCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联的用户')
    content = models.CharField(max_length=100, verbose_name='单词内容')
    # 单词解释,调用gpt生成多个解释，然后用户进行选择，填充到单词卡，用户可以填写自定义的备注
    explain = models.CharField(max_length=100, verbose_name='单词解释', null=True, blank=True)
    # 单词备注
    remark = models.CharField(max_length=100, verbose_name='单词备注', null=True, blank=True)
    # 场景例句
    sentence = models.TextField(max_length=500, verbose_name='场景例句', null=True, blank=True)
    # 例句翻译
    translation = models.TextField(max_length=500, verbose_name='例句翻译', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '单词卡'
        verbose_name_plural = verbose_name


class RootExplain(models.Model):
    """
    词根解释
    """
    word_card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='关联的单词')
    root = models.CharField(max_length=100, verbose_name='词根')
    explain = models.TextField(max_length=500, verbose_name='词根解释')
    cognates_description = models.TextField(max_length=500, verbose_name='补充描述同根词', null=True, blank=True)

    class Meta:
        verbose_name = '词根解释'
        verbose_name_plural = verbose_name


class WordUsage(models.Model):
    """
    单词用法
    """
    word_card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='关联的单词')
    content = models.TextField(max_length=50, verbose_name='内容')
    translation = models.TextField(max_length=50, verbose_name='翻译')
    example_sentence = models.TextField(max_length=500, verbose_name='例句')

    class Meta:
        verbose_name = '单词用法'
        verbose_name_plural = verbose_name
