from .models import Item
from .repository import Repository

class Usecase:
    def __init__(self, repository: Repository):
        self._repository = repository

    def delete(self, item: Item):
        try:
            self._repository.delete(item)
        except Exception as e:
            raise SystemError from e
