from .base import BaseRepository
from django.contrib.auth import get_user_model


class UserRepository(BaseRepository):
    model = get_user_model()

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create_user(**kwargs)
