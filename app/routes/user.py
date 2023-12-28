from fastapi import APIRouter, Depends
from app.schemas.user import FullUserProfile, MultipleUsersResponse, CreateUserResponse
from app.services.user import UserService
import logging
from app.dependencies import rate_limit

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)-6s %(name)-15s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    filename="log.txt",
)
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
logger.addHandler(console)




def create_user_router() -> APIRouter:
    user_router = APIRouter(
                            prefix="/user",
                            tags=["user"],
                            dependencies=[Depends(rate_limit)]
                            )
    user_service = UserService()

    @user_router.get("/all", response_model=MultipleUsersResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 2):
        users, total = await user_service.get_all_users_with_pagination(start, limit)
        formatted_users = MultipleUsersResponse(users=users, total=total)
        return formatted_users

    @user_router.get("/{user_id}", response_model=FullUserProfile)
    async def get_user_by_id(user_id: int):
        full_user_profile = await user_service.get_user_info(user_id)

        return full_user_profile

    @user_router.put("/{user_id}")
    async def update_user(user_id: int, full_profile_info: FullUserProfile):
        await user_service.create_update_user(full_profile_info, user_id)
        return None

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):
        logger.info(f"About to delete user_id: {user_id}")
        #try:
        await user_service.delete_user(user_id)
        #except KeyError:
        #    raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")

    @user_router.post("/", response_model=CreateUserResponse, status_code=201)
    async def add_user(full_profile_info: FullUserProfile):
        user_id = await user_service.create_update_user(full_profile_info)
        print("doc string:", user_service.create_update_user.__doc__)
        created_user = CreateUserResponse(user_id=user_id)
        return created_user

    return user_router