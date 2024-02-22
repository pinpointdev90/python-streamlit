from sample.exceptions import sampleError


class NotFoundError(sampleError):
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
