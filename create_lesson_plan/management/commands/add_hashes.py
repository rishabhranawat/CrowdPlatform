from django.core.management.base import BaseCommand

from create_lesson_plan.models import OfflineDocument

import hashlib

class Command(BaseCommand):
    
    def add_hashesh(self):
        all_docs = OfflineDocument.objects.all()
        for doc in all_docs:
            content = doc.content
            if(content != 'pdf attached' or content != 'doc attached'):
                m = hashlib.sha256()
                m.update(content)
                doc.content_hash = m.digest()
                doc.save()

    def handle(self, *args, **options):
        print("here")
