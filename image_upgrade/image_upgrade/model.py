from typing import Optional, types
from dataclasses import dataclass, field, fields, asdict, is_dataclass
import re
from importlib import import_module


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
            match = re.search(r"list\[(.*?)\]", str(f_info.type))
            if match:
                module_path, object_name = match.group(1).rsplit(".", 1)
                dc = getattr(import_module(module_path), object_name)
                if is_dataclass(dc) and isinstance(f_value, list):
                    dcl = []
                    for l_value in f_value:
                        if isinstance(l_value, dc):
                            dcl.append(l_value)
                        if isinstance(l_value, dict):
                            dcl.append(dc(**l_value))
                        else:
                            raise TypeError(
                                f"Type mismatch for {f_info.name}. Expected list[{object_name}], got list[{type(l_value)}]."
                            )
                    setattr(self, f_info.name, dcl)
                else:
                    raise TypeError(
                        f"Type mismatch for {f_info.name}. Expected list[{object_name}], got {type(f_value)}."
                    )
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


@dataclass
@dataclass_nested
class DockerTagsResult:
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


@dataclass
@dataclass_nested
class DockerTagsPage:
    count: int
    results: list[DockerTagsResult]
    # Optional
    next: Optional[str] = None
    previous: Optional[str] = None
