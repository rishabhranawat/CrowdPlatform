from elasticsearch.client import IndicesClient
from django.conf import settings
from django.core.management.base import BaseCommand
from create_lesson_plan.models import lesson

class Command(BaseCommand):
	def handle(self, *args, **options):
		self.recreate_index()
		self.push_db_to_index()

	def recreate_index(self):
		indices_client = IndicesClient(client=settings.ES_CLIENT)
		index_name = lesson._meta.es_index_name
		if(indices_client.exists(index_name)):
			indices_client.delete(index = index_name)
		indices_client.create(index=index_name)
		indices_client.put_mapping(
			doc_type=lesson._meta.es_type_name,
			body = lesson._meta.es_mapping,
			index=index_name
		)

	def push_db_to_index(self):
		data = [
			self.convert_for_bulk(s, 'create') for s in lesson.objects.all()
		]
		bulk(client=settings.ES_CLIENT, actions=data, stats_only=True)

	def convert_for_bulk(self, django_object, action=None):
		data = django_object.es_repr()
		metadata = {
			'_op_type':action,
			'_index': django_object._meta.es_index_name,
			"type": django_object._meta.es_type_name
		}
		data.update(**metadata)
		return data

	def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        data['_id'] = self.pk
        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data
    
    def field_es_repr(self, field_name):
        config = self._meta.es_mapping['properties'][field_name]
        if hasattr(self, 'get_es_%s' % field_name):
            field_es_value = getattr(self, 'get_es_%s' % field_name)()
        else:
            if config['type'] == 'object':
                related_object = getattr(self, field_name)
                field_es_value = {}
                field_es_value['_id'] = related_object.pk
                for prop in config['properties'].keys():
                    field_es_value[prop] = getattr(related_object, prop)
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value

    # def get_es_name_complete(self):
    #     return {
    #         "input": [self.first_name, self.last_name],
    #         "output": "%s %s" % (self.first_name, self.last_name),
    #         "payload": {"pk": self.pk},
    #     }
    # def get_es_course_names(self):
    #     if not self.courses.exists():
    #         return []
    #     return [c.name for c in self.courses.all()]