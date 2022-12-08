from fastapi import APIRouter
from config.database import *
from models.motorModel import Motor
from schemas.motorSchemas import motors_parser, motors_serializer
from schemas.bbmSchemas import *
from fastapi import FastAPI, HTTPException, Depends, Request,status
from auth.hash_password import Hash
from auth.jwt_handler import create_access_token
from auth.authenticate import get_current_user
from config.database import collection_user
from models.userModel import User
from auth.connect import *
from enum import Enum

class bbmModel(str, Enum):
    Pertamax_Turbo = "Pertamax Turbo"
    Pertamax = "Pertamax"
    Pertalite = "Pertalite"

motor_router = APIRouter()

@motor_router.get("/motors", tags=["motor"])
async def get_motors(current_user:User = Depends(get_current_user)):
    motors = motors_serializer(collection_name.find())
    return {"status": "ok", "data": motors}

@motor_router.get("/motors/search-nama/{nama_motor}", tags=["motor"])
async def get_motors_by_name(nama_motor: str, current_user:User = Depends(get_current_user)):
    return motors_serializer(collection_name.find({"nama_motor": nama_motor}))

@motor_router.get("/motors/harga-bulanan/{nama_motor}", tags=["motor"])
async def get_monthly_bbm_outcome(nama_motor: str, km: float, current_user:User = Depends(get_current_user)):
    harga = {'harga':''}
    motor = motors_parser(collection_name.find_one({"nama_motor": nama_motor}))
    jarak = km
    kmperliter = motor['kmperliter']
    bensin = 10000
    harga['harga'] = jarak / kmperliter * bensin * 30
    return harga

# @motor_router.get("/motors/harga-bulanan-bbm/{nama_motor}", tags=["motor"])
# async def get_monthly_bbm_outcome_bbmtype(nama_motor: str, jangkauan_km_perhari: float, lokasi: str, jenis_bbm: str, current_user:User = Depends(get_current_user)):
#     harga = {'harga':''}
#     motor = motors_parser(collection_name.find_one({"nama_motor": nama_motor}))
#     jarak = jangkauan_km_perhari
#     kmperliter = motor['kmperliter']
#     bbm = bbm_parser(collection_bbm.find_one({"Lokasi": lokasi, "BBM": jenis_bbm}))
#     bensin = bbm['Harga']
#     harga['harga'] = jarak / kmperliter * bensin * 30
#     return harga

@motor_router.get("/motors/harga-bulanan-bbm/{nama_motor}", tags=["motor"])
async def get_monthly_bbm_outcome_bbmtype(nama_motor: str, jangkauan_km_perhari: float, lokasi: str, jenis_bbm: bbmModel, current_user:User = Depends(get_current_user)):
    harga = {'harga':''}
    motor = motors_parser(collection_name.find_one({"nama_motor": nama_motor}))
    jarak = jangkauan_km_perhari
    kmperliter = motor['kmperliter']
    if jenis_bbm is bbmModel.Pertamax_Turbo:
        bbmtype = "Pertamax Turbo"
    elif jenis_bbm is bbmModel.Pertamax:
        bbmtype = "Pertamax"
    elif jenis_bbm is bbmModel.Pertalite:
        bbmtype = "Pertalite"
    bbm = bbm_parser(collection_bbm.find_one({"Lokasi": lokasi, "BBM": bbmtype}))
    bensin = bbm['Harga']
    harga['harga'] = jarak / kmperliter * bensin * 30
    return harga

@motor_router.post("/motors", tags=["motor"])
def add_motor(motor: Motor, user:User = Depends(get_current_user)):
    _id = collection_name.insert_one(dict(motor))
    motor = motors_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data":motor}

@motor_router.get("/motors/harga-bulanan-prediksi/{nama_motor}", tags=["motor"])
async def get_monthly_bbm_outcome_prediction(jangkauan_km_perhari: float, current_user:User = Depends(get_current_user)):
    harga = {'harga':''}
    motors = motors_serializer(collection_name.find())
    kmperlitertotal = 0
    for motor in motors:
        kmperliter = motor['kmperliter']
        kmperlitertotal += kmperliter
    konsumsi_bensin = kmperlitertotal / len(motors)
    jarak = jangkauan_km_perhari
    bensin = 10000
    harga['harga'] = jarak / konsumsi_bensin * bensin * 30
    return harga

@motor_router.put("/motors/update/{nama_motor}", tags=["motor"])
def update_harga_motor(nama_motor: str, kmperliter_baru: float, current_user:User = Depends(get_current_user)):
    indicator = {"nama_motor": nama_motor }
    newvalues = { "$set": { "kmperliter": kmperliter_baru } }

    jumlah = collection_name.count_documents({"nama_motor": nama_motor})

    if (jumlah == 0):
        return{'message': 'Tipe motor yang Anda masukkan salah. Silakan masukkan tipe motor yang benar'}

    collection_name.update_one(indicator, newvalues)
    return({"motor": "update success"})

@motor_router.delete("/motor/delete/{nama_motor}", tags=["motor"])
def delete_motor(nama_motor: str, current_user:User = Depends(get_current_user)):
    jumlah = collection_name.count_documents({"nama_motor": nama_motor})

    if (jumlah == 0):
        return{'message': 'Tipe motor yang Anda masukkan salah. Silakan masukkan tipe motor yang benar'}

    delete = collection_name.delete_one({"nama_motor": nama_motor})
    return {"motor": "delete success"}

@motor_router.get("/bbm", tags=["bbm"])
async def get_motors(current_user:User = Depends(get_current_user)):
    motors = bbm_serializer(collection_bbm.find())
    return {"status": "ok", "data": motors}

@motor_router.get("/bbm/search-lokasi/{lokasi}", tags=["bbm"])
async def get_motors_by_name(lokasi: str, current_user:User = Depends(get_current_user)):
    return bbm_serializer(collection_bbm.find({"Lokasi": lokasi}))


@motor_router.put("/bbm/update/{lokasi}", tags=["bbm"])
def update_harga_bbm(lokasi: str, bbm: str,  harga: int, current_user:User = Depends(get_current_user)):
    indicator = {"Lokasi": lokasi , "BBM": bbm}
    newvalues = { "$set": { "Harga": harga } }

    jumlah = collection_bbm.count_documents({"Lokasi": lokasi })

    if (jumlah == 0):
        return{'message': 'Lokasi yang Anda masukkan salah. Silakan masukkan tipe motor yang benar'}
    
    jumlah1 = collection_bbm.count_documents({"BBM": bbm})

    if (jumlah1 == 0):
        return{'message': 'Tipe bbm yang Anda masukkan salah. Silakan masukkan tipe motor yang benar'}

    collection_bbm.update_one(indicator, newvalues)
    return({"motor": "update success"})

@motor_router.get("/motors/harga-bulanan-total/{nama_motor}", tags=["motor"])
async def get_monthly_total_outcome(nama_motor: str, jangkauan_km_perhari: float, lokasi: str, jenis_bbm: bbmModel,  bunga: float, tenor: int, down_payment: int,  current_user:User = Depends(get_current_user)):
    cicilans = getCicilan(nama_motor, bunga, tenor, down_payment)
    totalcicilan = cicilans['cicilan']
    harga = {'harga':''}
    motor = motors_parser(collection_name.find_one({"nama_motor": nama_motor}))
    jarak = jangkauan_km_perhari
    kmperliter = motor['kmperliter']
    if jenis_bbm is bbmModel.Pertamax_Turbo:
        bbmtype = "Pertamax Turbo"
    elif jenis_bbm is bbmModel.Pertamax:
        bbmtype = "Pertamax"
    elif jenis_bbm is bbmModel.Pertalite:
        bbmtype = "Pertalite"
    bbm = bbm_parser(collection_bbm.find_one({"Lokasi": lokasi, "BBM": bbmtype}))
    bensin = bbm['Harga']
    hargabensin = jarak / kmperliter * bensin * 30
    harga['harga'] = hargabensin + totalcicilan
    return harga
    