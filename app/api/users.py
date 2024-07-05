from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED



router = APIRouter()


@router.get(
    path='/me',
    response_model=s.UserModelRead,
    status_code=HTTP_200_OK,
    summary='Get current user',
)
async def get_me(current_user: s.UserModelRead = Depends(get_current_user)) -> s.UserModelRead:
    """Get current user.

    Args:
        current_user (s.UserModelRead, optional): Current user.

    Returns:
        s.UserModelRead: Current user."""
    return current_user







@router.post(
    path='',
    response_model=s.UserModelRead,
    status_code=HTTP_201_CREATED,
    summary='Add new user',
)
async def create_user(
    user_data: s.UserModelCreate,
    user_service: UserService = Depends(get_user_service),
    curr_user: User = Depends(get_current_user),
) -> s.UserModelRead:
    """Add new user instance.

    Args:
        user_data (s.UserModelCreate): User data.
        user_service (UserService, optional): UserService instance.
        curr_user (User, optional): Current user.

    Returns:
        s.UserModelRead: Created user."""
    return await user_service.create(user_data, curr_user)


@router.patch(
    path='/{user_id}',
    response_model=s.UserModelRead,
    summary='Change user'
)
async def update_user(
    user_id: int,
    user_data: s.UserModelChange,
    user_service: UserService = Depends(get_user_service),
    curr_user: User = Depends(get_current_user),
) -> s.UserModelRead:
    """Edit user.

    Args:
        user_id (int): User id.
        user_data (s.UserModelChange): User data.
        user_service (UserService, optional): UserService instance.
        curr_user (User, optional): Current user.

    Returns:
        s.UserModelRead: Edited user."""
    return await user_service.update(user_id, user_data, curr_user)


@router.delete(
    path='/{user_id}',
    status_code=HTTP_200_OK,
    summary='Delete user',
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    curr_user: User = Depends(get_current_user),
) -> str:
    """Delete user

    Args:
        user_id (int): User id.
        user_service (UserService, optional): UserService instance.
        curr_user (User, optional): Current user.

    Returns:
        str: Message about success."""
    return await user_service.delete(user_id, curr_user)
