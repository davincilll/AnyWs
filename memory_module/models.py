from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from card_module.models.WordCard import WordCard


class MemoryPhaseEnum(models.IntegerChoices):
    """
    记忆阶段枚举
    1-5为正常阶段，-1为无需复习，-2为记忆完成
    """

    NO_NEED_REVIEW = -1, _('无需复习')
    MEMORY_COMPLETE = -2, _('记忆完成')
    INITIAL = 0, _('初始阶段，刚加入')
    PHASE_1_COMPLETE_LEARN = 1, _('阶段1 完成学习，距离下次复习还有1天')
    PHASE_2_COMPLETE_FIRST_REVIEW = 2, _('阶段2 完成第一次复习，距离下次复习还有3天')
    PHASE_3_COMPLETE_SECOND_REVIEW = 3, _('阶段3 完成第二次复习，距离下次复习还有7天')
    PHASE_4_COMPLETE_THIRD_REVIEW = 4, _('阶段4 完成第三次复习，距离下次复习还有14天')
    PHASE_5_COMPLETE_FOURTH_REVIEW = 5, _('阶段5 完成第四次复习，距离下次复习还有30天')


# Create your models here.
def get_review_interval(memory_phase):
    if memory_phase == MemoryPhaseEnum.PHASE_1_COMPLETE_LEARN:
        return 1
    if memory_phase == MemoryPhaseEnum.PHASE_2_COMPLETE_FIRST_REVIEW:
        return 3
    if memory_phase == MemoryPhaseEnum.PHASE_3_COMPLETE_SECOND_REVIEW:
        return 7
    if memory_phase == MemoryPhaseEnum.PHASE_4_COMPLETE_THIRD_REVIEW:
        return 14
    if memory_phase == MemoryPhaseEnum.PHASE_5_COMPLETE_FOURTH_REVIEW:
        return 30


class MemorySchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联的用户')
    word_card = models.OneToOneField(WordCard, on_delete=models.CASCADE, related_name='review_schedule',
                                     verbose_name='单词卡')
    memory_phase = models.IntegerField(verbose_name='记忆阶段', choices=MemoryPhaseEnum.choices)
    next_review_date = models.DateTimeField(verbose_name='下次复习时间', null=True, blank=True)
    last_reviewed_date = models.DateTimeField(null=True, blank=True, verbose_name='上次复习时间')

    def upgrade(self):
        """
        升级记忆阶段
        """
        if self.memory_phase == MemoryPhaseEnum.PHASE_5_COMPLETE_FOURTH_REVIEW:
            self.memory_phase = MemoryPhaseEnum.MEMORY_COMPLETE
            self.next_review_date = None
            self.last_reviewed_date = timezone.now()
        else:
            self.memory_phase += 1
        review_interval = get_review_interval(self.memory_phase)
        self.last_reviewed_date = timezone.now()
        self.next_review_date = self.last_reviewed_date + timedelta(days=review_interval)
        self.save()

    def no_need_review(self):
        """
        无需复习
        """
        self.memory_phase = MemoryPhaseEnum.NO_NEED_REVIEW
        self.last_reviewed_date = timezone.now()
        self.next_review_date = None
        self.save()

    def learn(self):
        """
        学习单词
        """
        self.memory_phase = MemoryPhaseEnum.PHASE_1_COMPLETE_LEARN
        self.last_reviewed_date = timezone.now()
        self.next_review_date = timezone.now() + get_review_interval(self.memory_phase)
        self.save()
    def forget(self):
        """
        忘记单词
        """
        self.memory_phase = MemoryPhaseEnum.INITIAL
        self.last_reviewed_date = None
        self.next_review_date = None
        self.save()

    class Meta:
        verbose_name = '记忆计划'
        verbose_name_plural = verbose_name
