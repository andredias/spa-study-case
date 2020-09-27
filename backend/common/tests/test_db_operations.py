from typing import Optional

from pydantic import BaseModel

from app.models import diff_models  # isort:skip


def test_diff_models():

    class A(BaseModel):
        id: int
        name: str
        value: int
        email: str

    class B(BaseModel):
        name: Optional[str]
        value: Optional[str]
        email: Optional[str]

    a1 = A(id=1, name='A', value=2, email='fulano@email.com')
    a2 = A(id=1, name='B', value=3, email='fulano@email.com')
    assert diff_models(a1, a2) == dict(name='B', value=3)
    assert diff_models(a2, a1) == dict(name='A', value=2)

    b = B(id=1, name='A', email='a@email.com')
    assert diff_models(a1, b) == dict(email='a@email.com')
