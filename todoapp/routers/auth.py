from fastapi import APIRouter

router = APIRouter(tags=['Authentication'])

@router.get('/auth')
async def get_user():
    return {"User Authenticated"}