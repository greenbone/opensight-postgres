from typing import Optional, types
from dataclasses import dataclass, field, fields, asdict, is_dataclass
import re


def _dataclass_nested(self):
    """Initializes nested data classes.

    Iterates through each field in the data class. If a field should be a data class
    and its value is a dictionary, it initializes the nested data class.
    Raises a TypeError for type mismatches. Calls the '___post_init___' method after
    initialization if present.
    """

    for f_info in fields(self):
        f_value = getattr(self, f_info.name)
        if isinstance(f_info.type, types.GenericAlias):
            # TODO dict[Any, DataClass] GenericAlias
            # Try to create a dataclass from an list GenericAlias
            # This is tricky and not the best solution
            match = re.search(r"list\[.*\.(.*?)\]", str(f_info.type))
            if match:
                dc = globals().get(match.group(1))
                if is_dataclass(dc) and isinstance(f_value, list):
                    setattr(self, f_info.name, [dc(**l) for l in f_value])
        elif isinstance(f_value, f_info.type):
            continue
        elif is_dataclass(f_info.type) and isinstance(f_value, dict):
            setattr(self, f_info.name, f_info.type(**f_value))
        else:
            raise TypeError(
                f"Type mismatch for {f_info.name}. Expected {f_info.type}, got {type(f_value)}."
            )
    if hasattr(self, "___post_init___"):
        self.___post_init___()


def dataclass_nested(cls):
    """Extends '__post_init__' to initialize nested data classes by replacing it
    with '_dataclass_deep_init'. If '__post_init__' exists, it is renamed
    to '___post_init___'.
    """

    if hasattr(cls, "__post_init__"):
        setattr(cls, "___post_init___", getattr(cls, "__post_init__"))
    setattr(cls, "__post_init__", _dataclass_nested)
    return cls


@dataclass
@dataclass_nested
class DockerTagsImage:
    architecture: str = field(default_factory=str)
    features: str = field(default_factory=str)
    variant: Optional[str] = field(default_factory=str)
    digest: str = field(default_factory=str)
    os: str = field(default_factory=str)
    os_features: str = field(default_factory=str)
    os_version: Optional[str] = field(default_factory=str)
    size: int = field(default_factory=int)
    status: str = field(default_factory=str)
    last_pulled: Optional[str] = field(default_factory=str)
    last_pushed: Optional[str] = field(default_factory=str)


@dataclass
@dataclass_nested
class DockerTagsResult:
    creator: int = field(default_factory=int)
    id: int = field(default_factory=int)
    images: list[DockerTagsImage] = field(default_factory=list)
    last_updated: str = field(default_factory=str)
    last_updater: int = field(default_factory=str)
    last_updater_username: str = field(default_factory=str)
    name: str = field(default_factory=str)
    repository: int = field(default_factory=int)
    full_size: int = field(default_factory=int)
    v2: bool = field(default_factory=bool)
    tag_status: str = field(default_factory=str)
    tag_last_pulled: Optional[str] = field(default_factory=str)
    tag_last_pushed: Optional[str] = field(default_factory=str)
    media_type: str = field(default_factory=str)
    content_type: str = field(default_factory=str)
    digest: str = field(default_factory=str)


@dataclass
@dataclass_nested
class DockerTagsPage:
    count: int = field(default_factory=int)
    next: Optional[str] = field(default_factory=str)
    previous: Optional[str] = field(default_factory=str)
    results: list[DockerTagsResult] = field(default_factory=list)
