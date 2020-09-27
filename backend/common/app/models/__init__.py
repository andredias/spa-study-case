from typing import MutableMapping

from pydantic import BaseModel
from sqlalchemy import MetaData

metadata = MetaData()

from . import user  # noqa: E402

__all__ = [
    'user',
]


def diff_models(from_: BaseModel, to_: BaseModel) -> MutableMapping:
    '''
    Return a dict with differences of the second in relation to the first model.
    Useful for getting only the fields that have changed before an update, for example.
    '''
    from_dict = from_.dict()
    to_dict = to_.dict(exclude_unset=True)
    return {k: v for k, v in to_dict.items() if from_dict.get(k) != v}
