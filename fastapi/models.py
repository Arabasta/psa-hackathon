from pydantic import BaseModel
from typing import List

# unused
class Submission(BaseModel):
    image_caption: str
    employees: List[str]
