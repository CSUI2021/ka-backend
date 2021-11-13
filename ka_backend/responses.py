import typing as t

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class StudentSummary(BaseModel):
    username: str
    nama: str
    jurusan: t.Literal["ilmu_komputer", "sistem_informasi"]
    foto_diri: t.Optional[str]
    house_name: t.Optional[str]
    is_2021: bool


class Story(BaseModel):
    id: int
    title: str
    detail: str
    foto: t.List[str]


class Competition(BaseModel):
    id: int
    nama: str
    foto: t.Optional[str]
    link: str


class SIG(BaseModel):
    id: int
    nama: str
    detail: str
    foto: t.Optional[str]
    is_it_interest: bool


class House(BaseModel):
    id: int
    codename: str
    nama: str


class Student(BaseModel):
    username: str

    # Data diri
    nama: str
    jurusan: t.Literal["ilmu_komputer", "sistem_informasi"]
    ttl: str
    hobi: str

    # Social media
    twitter: t.Optional[str]
    line: t.Optional[str]
    instagram: t.Optional[str]

    foto_diri: t.Optional[str]
    video_diri: t.Optional[str]
    house: House
    house_led: t.Optional[House]

    message: str
    about: str
    interests: t.List[str]
