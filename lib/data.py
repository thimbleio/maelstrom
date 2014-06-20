from base import Base
from uuid import uuid4

class Data(Base):
    __tablename__ = "data"

    defaults = {
        "id" : uuid4(),
        "contents" : ""
    }

    def __init__(self, *args, **kwargs):
        self.update_data(**self.defaults)
        Base.__init__(self, *args, **kwargs)