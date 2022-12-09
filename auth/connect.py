from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from enum import Enum

class Tenor(str, Enum):
    dua_belas_bulan = "12"
    delapan_belas_bulan = "18"
    dua_puluh_empat = "24"
    tiga_puluh = "30"

def get_bearer_token():
    url = 'https://motorvic.wonderfulisland-bafbc83c.centralus.azurecontainerapps.io/login'
    data = {"username": "admin", "password": "admin"}
    response = requests.post(url, data=data)
    jsonresponse = response.json()
    bearertoken = str(jsonresponse['access_token'])
    return bearertoken


def format_get(url: str):
    link = url
    headers = {"Authorization": f'Bearer {get_bearer_token()}'}
    response = requests.get(link, headers=headers)
    jsonresponse = response.json()
    return jsonresponse

def getCicilan(jenis_motor: str, bunga: float, tenor: Tenor, down_payment: int):
    url = f'https://motorvic.wonderfulisland-bafbc83c.centralus.azurecontainerapps.io/motor/cicilan/{jenis_motor}?bunga={bunga}&tenor={tenor}&down_payment={down_payment}'
    return format_get(url)