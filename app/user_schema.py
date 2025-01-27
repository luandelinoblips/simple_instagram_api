from typing import List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class Post:
    _id: str
    type: str
    caption: str
    media_url: str
    permalink: str
    timestamp: str
    like_count: int
    comments_count: int
    is_video: bool
    has_audio: bool

    def to_json(self) -> dict:
        return asdict(self)


@dataclass
class User:
    _id: str
    name: str
    username: str
    img_url: str
    email: str
    bio: str
    followers: int
    following: int
    num_posts: int
    category_name: str
    posts: Optional[List[Post]] = field(default_factory=list)

    def to_json(self) -> dict:
        return asdict(self)
