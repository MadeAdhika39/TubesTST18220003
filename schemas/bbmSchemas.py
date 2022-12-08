from enum import Enum

def bbm_parser(bbm) -> dict:
    return{
        "id": str(bbm["_id"]),
        "Lokasi": bbm["Lokasi"],
        "BBM": bbm["BBM"],
        "Harga": bbm["Harga"]
    }

def bbm_serializer(bbms) -> list:
    return [bbm_parser(bbm) for bbm in bbms]

class bbmModel(str, Enum):
    Pertamax_Turbo = "Pertamax Turbo"
    Pertamax = "Pertamax"
    Pertalite = "Pertalite"
