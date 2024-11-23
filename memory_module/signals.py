from django.db.models.signals import post_save
from django.dispatch import receiver

from card_module.models.WordCard import WordCard
from memory_module.models import MemorySchedule


# @receiver(post_save, sender=WordCard)
# def addMemorySchedule(sender, instance, created, **kwargs):
#     if created:
#         MemorySchedule.objects.create(user=instance.user_id, word_card=instance)
