from django.contrib.auth.models import User
from django.db import models


class WordCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联的用户')
    content = models.CharField(max_length=100, verbose_name='单词内容')
    # 单词解释,调用gpt生成多个解释，然后用户进行选择，填充到单词卡，用户可以填写自定义的备注
    explanatory_in_chinese = models.CharField(max_length=100, verbose_name='单词解释用中文')
    explanatory_in_english = models.CharField(max_length=100, verbose_name='单词翻译用英文',null=True, blank=True)
    # 单词备注
    remark_of_user = models.CharField(max_length=100, verbose_name='单词备注', null=True, blank=True)
    # 场景例句
    scene_example_sentence = models.TextField(max_length=500, verbose_name='场景例句', null=True, blank=True)
    # 例句翻译
    translation_of_sentence = models.TextField(max_length=500, verbose_name='例句翻译', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True, blank=True)

    class Meta:
        verbose_name = '单词卡'
        verbose_name_plural = verbose_name


class RootExplain(models.Model):
    """
    词根解释
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联的用户')
    word_card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='关联的单词',
                                  related_name='root_explains')
    root = models.CharField(max_length=100, verbose_name='词根')
    explain = models.TextField(max_length=500, verbose_name='词根解释')
    cognates_description = models.TextField(max_length=500, verbose_name='补充描述')

    class Meta:
        verbose_name = '词根解释'
        verbose_name_plural = verbose_name


class UsefulPhraseUsingThisVocabulary(models.Model):
    """
    使用该词汇的相关短语
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联的用户')
    word_card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='关联的单词',
                                  related_name='word_usages')
    content = models.TextField(max_length=50, verbose_name='内容')
    translation = models.TextField(max_length=50, verbose_name='翻译')
    scene_example_sentence = models.TextField(max_length=500, verbose_name='例句')

    class Meta:
        verbose_name = '使用该词汇的相关短语'
        verbose_name_plural = verbose_name
