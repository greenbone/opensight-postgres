import re
from typing import Optional

from pydantic import BaseModel


class DockerTagsImage(BaseModel):
    architecture: str
    features: str
    os: str
    os_features: str
    size: int
    status: str
    # Optional
    digest: Optional[str] = None
    os_version: Optional[str] = None
    last_pulled: Optional[str] = None
    last_pushed: Optional[str] = None
    variant: Optional[str] = None


class DockerTagsResult(BaseModel):
    creator: int
    id: int
    images: list[DockerTagsImage]
    last_updated: str
    last_updater: int
    last_updater_username: str
    name: str
    repository: int
    full_size: int
    v2: bool
    tag_status: str
    media_type: str
    content_type: str
    # Optional
    digest: Optional[str] = None
    tag_last_pulled: Optional[str] = None
    tag_last_pushed: Optional[str] = None


class DockerTagsPage(BaseModel):
    count: int
    results: list[DockerTagsResult]
    # Optional
    next: Optional[str] = None
    previous: Optional[str] = None
