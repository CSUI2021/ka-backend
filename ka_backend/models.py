from ka_backend.helper.database import BaseMeta
import ormar
from typing import TYPE_CHECKING, List
from pydantic.typing import ForwardRef

HouseRef = ForwardRef("House")
StudentRef = ForwardRef("Student")


class Student(ormar.Model):
    class Meta(BaseMeta):
        tablename = "students"

    npm = ormar.Integer(primary_key=True)

    # Data diri
    nama: str = ormar.String(max_length=100)
    jurusan: str = ormar.String(
        max_length=32, choices=["ilmu_komputer", "sistem_informasi"]
    )
    ttl: str = ormar.String(max_length=100)
    hobi: str = ormar.String(max_length=50)

    # Social media
    twitter: str = ormar.String(max_length=16, nullable=True)
    line: str = ormar.String(max_length=50, nullable=True)
    instagram: str = ormar.String(max_length=32, nullable=True)
    karya: List[str] = ormar.JSON(nullable=True)  # type: ignore

    foto_diri: str = ormar.Text()
    video_diri: str = ormar.Text()
    house = ormar.ForeignKey(HouseRef, related_name="members")
    house_led = ormar.ForeignKey(HouseRef, related_name="ketua")


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
    foto: str = ormar.Text(nullable=True)
    is_it_interest = ormar.Boolean(default=True)


class Competition(ormar.Model):
    class Meta(BaseMeta):
        tablename = "competitions"

    id: int = ormar.Integer(primary_key=True)
    nama: str = ormar.String(max_length=160)
    foto: str = ormar.Text(nullable=True)
    link: str = ormar.Text()


Student.update_forward_refs()
