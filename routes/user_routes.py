from fastapi import APIRouter, HTTPException, Depends
from repositories.userRepository import UserRepository
from models.user import User, UserRequest
from dependencies import get_user_repository

user_router = APIRouter()

@user_router.post("/", response_model=User)
async def create_user(user_data: UserRequest, user_repo: UserRepository = Depends(get_user_repository)):
    print(user_repo)
    new_user = user_repo.create(user_data)
    return new_user

@user_router.get("/", response_model=list)
async def get_all_users(user_repo: UserRepository = Depends(get_user_repository)):
    return user_repo.find_all()

@user_router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, update_request: UserRequest, user_repo: UserRepository = Depends(get_user_repository)):
    user = user_repo.update(user_id, update_request)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    success = user_repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
