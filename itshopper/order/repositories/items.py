from django.core.exceptions import ObjectDoesNotExist

from .base import BaseRepository
from order.models import Item


class ItemRepository(BaseRepository):
    model = Item

    @classmethod
    def contains_field_substring(cls, string: str):
        try:
            return cls.model.objects.filter(name__icontains=string)
        except ObjectDoesNotExist:
            return None
