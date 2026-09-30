from typing import Literal

from pydantic import BaseModel, Field


class QnARequest(BaseModel):
    question: str = Field(..., min_length=1)
    context: str = ""


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    length: Literal["short", "medium", "detailed"] = "medium"


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    topic: str
    difficulty: str
    quiz: list[QuizQuestion]


class Recommendation(BaseModel):
    title: str
    description: str
    action: str