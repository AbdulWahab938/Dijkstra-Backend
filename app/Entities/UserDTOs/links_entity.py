from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl, StringConstraints, field_validator


# ----------------------
# Input DTOs
# ----------------------
class CreateLinks(BaseModel):
    user_id: UUID
    portfolio_link: Optional[HttpUrl] = None
    github_user_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    github_link: HttpUrl
    linkedin_user_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    linkedin_link: HttpUrl
    leetcode_user_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    leetcode_link: HttpUrl
    orcid_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    orcid_link: HttpUrl

    # Validation example: ensure usernames are lowercase
    @field_validator("github_user_name", "linkedin_user_name", "leetcode_user_name", "orcid_id")
    def strip_and_lowercase(cls, v: str) -> str:
        return v.strip()


class UpdateLinks(BaseModel):
    portfolio_link: Optional[HttpUrl] = None
    github_user_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]] = None
    github_link: Optional[HttpUrl] = None
    linkedin_user_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]] = None
    linkedin_link: Optional[HttpUrl] = None
    leetcode_user_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]] = None
    leetcode_link: Optional[HttpUrl] = None
    orcid_id: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]] = None
    orcid_link: Optional[HttpUrl] = None

    @field_validator("github_user_name", "linkedin_user_name", "leetcode_user_name", "orcid_id")
    def strip_if_not_none(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


# ----------------------
# Output DTOs
# ----------------------
class ReadLinks(BaseModel):
    id: UUID
    user_id: UUID
    portfolio_link: Optional[HttpUrl]
    github_user_name: str
    github_link: HttpUrl
    linkedin_user_name: str
    linkedin_link: HttpUrl
    leetcode_user_name: str
    leetcode_link: HttpUrl
    orcid_id: str
    orcid_link: HttpUrl
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  

# ----------------------
# Extended Output DTOs (if needed)
# ----------------------
class ReadLinksWithRelations(ReadLinks):
    # For future expansion: include User details if needed
    user: Optional["ReadUser"] = None

    class Config:
        from_attributes = True


# Avoid circular import by importing at the end
from Entities.UserDTOs.user_entity import ReadUser
ReadLinksWithRelations.model_rebuild()
