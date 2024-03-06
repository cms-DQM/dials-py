from pydantic import BaseModel


class OBaseModel(BaseModel):
    def cleandict(self):
        return {key: value for key, value in self.dict().items() if value is not None}
