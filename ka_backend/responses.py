import typing as t
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class StudentSummary(BaseModel):
    nama: str
    jurusan: t.Literal["ilmu_komputer", "sistem_informasi"]
    foto_diri: t.Optional[str]
    house_name: t.Optional[str]
