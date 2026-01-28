from pydantic import BaseModel, Field 
from typing import Optional, List, Dict, Any, Union


class Metadata(BaseModel):

    """ 
    This is a pydantic object for validating the output of the model
    """
    Summary: List[str] = Field(default_factory=list, description="Summary of document")
    Title: str
    Author: List[str]
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    Changes: str