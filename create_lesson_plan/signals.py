from create_lesson_plan.models import OfflineDocument
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=OfflineDocument)
def index_offline_document(sender, instance, **kwargs):
	instance.indexing()

