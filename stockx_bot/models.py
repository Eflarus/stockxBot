import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    user_id: int
    username: str | None
    name: str | None
    last_name: str | None
    created_at: datetime.datetime
    last_active_at: datetime.datetime | None


class ConversationData:
    def __init__(self):
        self.order_id = None
        self.user_id = None
        self.username = None
        self.first_name = None
        self.last_name = None
        self.photo_file_ids = []
        self.caption = None
        self.size = None
        self.promo = None
        self.created_at = datetime.datetime.now(datetime.timezone.utc)

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo_file_id': self.photo_file_ids,
            'caption': self.caption,
            'size': self.size,
            'promo': self.promo,
            'created_at': self.created_at
        }
