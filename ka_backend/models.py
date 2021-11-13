from typing import List, Optional

import ormar
from pydantic.typing import ForwardRef

from ka_backend.helper.database import BaseMeta

HouseRef = ForwardRef("House")
StudentRef = ForwardRef("Student")


class Student(ormar.Model):
    class Meta(BaseMeta):
        tablename = "students"

    npm = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=128, nullable=True)
    is_admin: bool = ormar.Boolean(default=False, nullable=False)

    # Data diri
    nama: str = ormar.String(max_length=100, nullable=True)
    jurusan: str = ormar.String(
        max_length=32,
        choices=["ilmu_komputer", "sistem_informasi"],
        nullable=True,
    )
    ttl: str = ormar.String(max_length=100, nullable=True)
    hobi: str = ormar.String(max_length=50, nullable=True)

    # Social media
    twitter: Optional[str] = ormar.String(max_length=32, nullable=True)
    line: Optional[str] = ormar.String(max_length=50, nullable=True)
    instagram: Optional[str] = ormar.String(max_length=32, nullable=True)

    foto_diri: Optional[str] = ormar.Text(nullable=True)
    video_diri: Optional[str] = ormar.Text(nullable=True)
    house = ormar.ForeignKey(HouseRef, related_name="members")
    house_led = ormar.ForeignKey(HouseRef, related_name="ketua")

    message: str = ormar.Text(nullable=True)
    about: str = ormar.Text(nullable=True)
    interests: List[str] = ormar.JSON(default="[]")  # type: ignore

    async def get_summary(self):
        house_name = None
        if self.house:
            if not self.house.nama:
                await self.house.load()
            house_name = self.house.nama

        return {
            "username": self.username,
            "nama": self.nama,
            "is_2021": self.npm >= 2100000000,
            "jurusan": self.jurusan,
            "foto_diri": self.foto_diri,
            "house_name": house_name,
        }


class House(ormar.Model):
    class Meta(BaseMeta):
        tablename = "houses"

    id: int = ormar.Integer(primary_key=True)
    nama: str = ormar.String(max_length=32)


class SIG(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sigs"

    id: int = ormar.Integer(primary_key=True)
    nama: str = ormar.String(max_length=160)
    detail: str = ormar.Text()
    foto: Optional[str] = ormar.Text(nullable=True)
    is_it_interest = ormar.Boolean(default=True)


class Competition(ormar.Model):
    class Meta(BaseMeta):
        tablename = "competitions"

    id: int = ormar.Integer(primary_key=True)
    nama: str = ormar.String(max_length=160)
    foto: Optional[str] = ormar.Text(nullable=True)
    link: str = ormar.Text()


class Story(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stories"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=128)
    detail: str = ormar.Text()
    foto: List[str] = ormar.JSON(default="[]")  # type: ignore


Student.update_forward_refs()
