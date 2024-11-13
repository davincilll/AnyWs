from django.db import models

from card_module.models.WordCard import WordCard

class MemoryPhaseEnum(models.IntegerChoices):
    """
    记忆阶段枚举类，用于表示单词卡的记忆阶段，包括：
    1. 初始阶段：单词卡新加入
    2. 无需复习，手动将单词卡设置为无需复习
    3. 学习完成，复习计划结束，可手动指定这个阶段
    4. 记忆完成
    5.
    """

# # Create your models here.
# class MemorySchedule(models.Model):
#     word_card = models.OneToOneField(WordCard, on_delete=models.CASCADE, related_name='review_schedule',
#                                      verbose_name='单词卡')
#     memory_phase = models.IntegerField(verbose_name='记忆阶段',)
#     next_review_date = models.DateTimeField(verbose_name='下次复习时间')
#     review_intervals = models.JSONField(verbose_name='复习间隔', default=list)  # 存储复习间隔（如：天数）
#     last_reviewed = models.DateTimeField(null=True, blank=True, verbose_name='上次复习时间')
#
#     def remember(self):
#         """
#         记住单词，即更新复习计划
#         """
#         self.last_reviewed = self.next_review_date
#         self.next_review_date = self.next_review_date + self.review_intervals[0]
#         self.review_intervals = self.review_intervals[1:]
#         self.save()
#
#     def review(self):
#
#     class Meta:
#         verbose_name = '复习计划'
#         verbose_name_plural = verbose_name
