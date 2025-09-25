from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID

from Settings.logging_config import setup_logging
from Entities.UserDTOs.links_entity import CreateLinks, ReadLinks, UpdateLinks
from Services.User.links_service import LinksService
from db import get_session
from Utils.Exceptions.user_exceptions import (
    UserNotFound,
    LinksNotFound,
    LinksAlreadyExists,
    GitHubUsernameNotFound,
)

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/links", tags=["Links"])


@router.post(
    "/",
    response_model=ReadLinks,
    responses={
        400: {"description": "User not found / GitHub username not found"},
        409: {"description": "Links already exist for this user"},
    },
)
def create_links(links_create: CreateLinks, session: Session = Depends(get_session)):
    service = LinksService(session)
    try:
        logger.info(f"Creating links for user ID: {links_create.user_id}")
        return service.create_links(links_create)
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GitHubUsernameNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LinksAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/{link_id}",
    response_model=ReadLinks,
    responses={
        404: {"description": "Links not found"},
    },
)
def get_links(link_id: UUID, session: Session = Depends(get_session)):
    service = LinksService(session)
    try:
        logger.info(f"Fetching links with ID: {link_id}")
        return service.get_links(link_id)
    except LinksNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/user/{user_id}",
    response_model=ReadLinks,
    responses={
        404: {"description": "Links not found for this user"},
    },
)
def get_links_by_user(user_id: UUID, session: Session = Depends(get_session)):
    service = LinksService(session)
    try:
        logger.info(f"Fetching links for user ID: {user_id}")
        return service.get_links_by_user_id(user_id)
    except LinksNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[ReadLinks])
def list_links(skip: int = 0, limit: int = 20, session: Session = Depends(get_session)):
    service = LinksService(session)
    logger.info(f"Listing links: skip={skip}, limit={limit}")
    return service.list_links(skip=skip, limit=limit)


@router.put(
    "/{link_id}",
    response_model=ReadLinks,
    responses={
        404: {"description": "Links not found"},
    },
)
def update_links(link_id: UUID, links_update: UpdateLinks, session: Session = Depends(get_session)):
    service = LinksService(session)
    try:
        logger.info(f"Updating links ID: {link_id}")
        return service.update_links(link_id, links_update)
    except LinksNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{link_id}",
    responses={
        200: {"description": "Links deleted successfully"},
        404: {"description": "Links not found"},
    },
)
def delete_links(link_id: UUID, session: Session = Depends(get_session)):
    service = LinksService(session)
    try:
        logger.info(f"Deleting links ID: {link_id}")
        message = service.delete_links(link_id)
        return {"detail": message}
    except LinksNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
