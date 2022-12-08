from pydantic import BaseModel, Field

class Motor(BaseModel):
    tipemotor: str = Field(default=None)
    kmperliter: float = Field(default=None)
    class Config:
        schema_extra = {
            "motor_demo" : {
                "tipemotor": "beat pop",
                "kmperliter": 39.0,
            }
        }