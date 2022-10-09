from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel


class ExternalUrls(BaseModel):
    spotify: str


class Artist(BaseModel):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class ExternalUrls1(BaseModel):
    spotify: str


class Image(BaseModel):
    height: int
    url: str
    width: int


class Item(BaseModel):
    album_type: str
    artists: List[Artist]
    available_markets: List[str]
    external_urls: ExternalUrls1
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class Albums(BaseModel):
    href: str
    items: List[Item]
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class ExternalUrls2(BaseModel):
    spotify: str


class Followers(BaseModel):
    href: Any
    total: int


class Image1(BaseModel):
    height: int
    url: str
    width: int


class Item1(BaseModel):
    external_urls: ExternalUrls2
    followers: Followers
    genres: List[str]
    href: str
    id: str
    images: List[Image1]
    name: str
    popularity: int
    type: str
    uri: str


class Artists(BaseModel):
    href: str
    items: List[Item1]
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class ExternalUrls3(BaseModel):
    spotify: str


class Artist1(BaseModel):
    external_urls: ExternalUrls3
    href: str
    id: str
    name: str
    type: str
    uri: str


class ExternalUrls4(BaseModel):
    spotify: str


class Image2(BaseModel):
    height: int
    url: str
    width: int


class Album(BaseModel):
    album_type: str
    artists: List[Artist1]
    available_markets: List[str]
    external_urls: ExternalUrls4
    href: str
    id: str
    images: List[Image2]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class ExternalUrls5(BaseModel):
    spotify: str


class Artist2(BaseModel):
    external_urls: ExternalUrls5
    href: str
    id: str
    name: str
    type: str
    uri: str


class ExternalIds(BaseModel):
    isrc: str


class ExternalUrls6(BaseModel):
    spotify: str


class Item2(BaseModel):
    album: Album
    artists: List[Artist2]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIds
    external_urls: ExternalUrls6
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[str]
    track_number: int
    type: str
    uri: str


class Tracks(BaseModel):
    href: str
    items: List[Item2]
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class ExternalUrls7(BaseModel):
    spotify: str


class Image3(BaseModel):
    height: Optional[int]
    url: str
    width: Optional[int]


class ExternalUrls8(BaseModel):
    spotify: str


class Owner(BaseModel):
    display_name: str
    external_urls: ExternalUrls8
    href: str
    id: str
    type: str
    uri: str


class Tracks1(BaseModel):
    href: str
    total: int


class Item3(BaseModel):
    collaborative: bool
    description: str
    external_urls: ExternalUrls7
    href: str
    id: str
    images: List[Image3]
    name: str
    owner: Owner
    primary_color: Any
    public: Any
    snapshot_id: str
    tracks: Tracks1
    type: str
    uri: str


class Playlists(BaseModel):
    href: str
    items: List[Item3]
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class Shows(BaseModel):
    href: str
    items: List[Any]
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class Episodes(BaseModel):
    href: str
    items: List
    limit: int
    next: str
    offset: int
    previous: Any
    total: int


class SearchResults(BaseModel):
    """Model for search results"""
    albums: Albums
    artists: Artists
    tracks: Tracks
    playlists: Playlists
    shows: Shows
    episodes: Episodes