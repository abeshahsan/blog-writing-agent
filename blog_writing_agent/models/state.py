import operator
from typing import Annotated, List, TypedDict
from typing_extensions import NotRequired

from .plan import Plan


class GraphState(TypedDict):
    topic: str
    sections: Annotated[List[str], operator.add]
    plan: NotRequired[Plan]
    final: NotRequired[str]
