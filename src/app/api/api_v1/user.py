import logging

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies.auth import CurrentUserDep, get_current_auth_admin
from app.api.dependencies.user import UserServiceDep, UserServiceTxDep
from app.schemas.user import UserRead, UserUpdate
from core.config import settings

log = logging.getLogger(__name__)
router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)


@router.get(
    "/me",
    summary="Get current user profile",
    description="Retrieve the authenticated user's profile information including personal details and verification status.",
    response_model=UserRead,
    responses={
        status.HTTP_200_OK: {
            "description": "Current user profile retrieved successfully",
            "model": UserRead,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
    },
)
async def get_me(
    current_auth_user: CurrentUserDep,
):
    """Get the current authenticated user's profile"""
    return current_auth_user


@router.get(
    "",
    summary="Get all users",
    description="Retrieve a list of all users in the system. This endpoint is restricted to administrators only.",
    response_model=list[UserRead],
    dependencies=[Depends(get_current_auth_admin)],
    responses={
        status.HTTP_200_OK: {
            "description": "List of all users retrieved successfully",
            "model": list[UserRead],
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Admin privileges required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "You are not authorized to perform this action",
                        "details": None,
                    }
                }
            },
        },
    },
)
async def get_all_users(
    user_service: UserServiceDep,
):
    """Get all users in the system (Admin only)"""
    return await user_service.get_all_users()


@router.get(
    "/{user_id}",
    summary="Get user by ID",
    description="Retrieve a specific user's profile by their unique ID. This endpoint is restricted to administrators only.",
    response_model=UserRead,
    dependencies=[Depends(get_current_auth_admin)],
    responses={
        status.HTTP_200_OK: {
            "description": "User profile retrieved successfully",
            "model": UserRead,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Admin privileges required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "You are not authorized to perform this action",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                        "details": {"user_id": 123},
                    }
                }
            },
        },
    },
)
async def get_user_by_id(
    user_id: int,
    user_service: UserServiceDep,
):
    """Get a specific user by their ID (Admin only)."""
    return await user_service.get_user_by_id(user_id)


@router.patch(
    "/me",
    summary="Update current user profile",
    description="Update the authenticated user's profile information",
    response_model=UserRead,
    responses={
        status.HTTP_200_OK: {
            "description": "User profile updated successfully",
            "model": UserRead,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Bad request",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Phone number already exists",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Phone number already exists",
                        "details": None,
                    }
                }
            },
        },
    },
)
async def update_me(
    user_data: UserUpdate,
    user_service: UserServiceTxDep,
    current_auth_user: CurrentUserDep,
):
    """Update the current authenticated user's profile"""
    return await user_service.update_user(current_auth_user.id, user_data)


@router.patch(
    "/{user_id}",
    summary="Update user profile",
    description="Update a user's profile information. Users can only update their own profile",
    response_model=UserRead,
    responses={
        status.HTTP_200_OK: {
            "description": "User profile updated successfully",
            "model": UserRead,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Bad request",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Permission denied - can only update own profile",
            "content": {
                "application/json": {
                    "example": {
                        "message": "You are not authorized to update this user",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Resource not found",
                        "details": {"user_id": 123},
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Phone number already exists",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Phone number already exists",
                        "details": None,
                    }
                }
            },
        },
    },
)
@router.delete(
    "/{user_id}",
    summary="Delete user",
    description="Permanently delete a user from the system. This endpoint is restricted to administrators only and cannot be undone.",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_auth_admin)],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted successfully",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid token",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Admin privileges required",
            "content": {
                "application/json": {
                    "example": {
                        "message": "You are not authorized to perform this action",
                        "details": None,
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                        "details": {"user_id": 123},
                    }
                }
            },
        },
    },
)
async def delete_user(
    user_id: int,
    user_service: UserServiceTxDep,
):
    """Delete a user from the system (Admin only)"""
    return await user_service.delete_user(user_id)
