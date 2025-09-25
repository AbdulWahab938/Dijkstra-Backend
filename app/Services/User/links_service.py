from uuid import UUID
from sqlmodel import Session
from typing import Optional
from Schema.SQL.Models.models import User, Github, Links
from Repository.User.links_repository import LinksRepository
from Entities.UserDTOs.links_entity import CreateLinks, UpdateLinks
from Utils.Exceptions.user_exceptions import (
    UserNotFound,
    GitHubUsernameNotFound,
    LinksNotFound,
    LinksAlreadyExists,
)

class LinksService:
    def __init__(self, session: Session):
        self.repo = LinksRepository(session)
        self.session = session

    def create_links(self, links_create: CreateLinks) -> Links:
        # 1️⃣ Check if user exists
        user = self.session.get(User, links_create.user_id)
        if not user:
            raise UserNotFound(links_create.user_id)

        # 2️⃣ Check if links already exist for this user
        existing = self.repo.get_by_user_id(links_create.user_id)
        if existing:
            raise LinksAlreadyExists(links_create.user_id)

        # 3️⃣ Validate github_user_name exists in Github table
        github_entry = self.session.get(Github, links_create.github_user_name)
        if not github_entry:
            raise GitHubUsernameNotFound(links_create.github_user_name)

        # 4️⃣ Create new Links entry
        links = Links(**links_create.dict(exclude_unset=True))
        return self.repo.create(links)

    def get_links(self, link_id: UUID) -> Links:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)
        return links

    def get_links_by_user_id(self, user_id: UUID) -> Links:
        links = self.repo.get_by_user_id(user_id)
        if not links:
            raise LinksNotFound(user_id)
        return links

    def list_links(self, skip: int = 0, limit: int = 20):
        return self.repo.list(skip=skip, limit=limit)

    def update_links(self, link_id: UUID, links_update: UpdateLinks) -> Links:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)

        update_data = links_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(links, key, value)
        return self.repo.update(links)

    def delete_links(self, link_id: UUID) -> str:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)
        self.repo.delete(links)
        return f"Links {link_id} deleted successfully"
