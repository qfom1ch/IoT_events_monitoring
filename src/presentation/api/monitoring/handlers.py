from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(prefix='/metrics', tags=['monitoring'])


@router.get('')
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
