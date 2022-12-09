from pydantic import BaseModel, Field

class Motor(BaseModel):
    nama_motor: str = Field(default=None)
    kmperliter: float = Field(default=None)
    class Config:
        schema_extra = {
            "motor_demo" : {
                "nama_motor": "beat pop",
                "kmperliter": 39.0,
            }
        }