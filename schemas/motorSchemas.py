def motors_parser(motor) -> dict:
    return{
        "id": str(motor["_id"]),
        "nama_motor": motor["nama_motor"],
        "kmperliter": motor["kmperliter"]
    }

def motors_serializer(motors) -> list:
    return [motors_parser(motor) for motor in motors]