from dataclasses import dataclass
from strenum import StrEnum
from langchain_openai import ChatOpenAI
import tiktoken
from tiktoken.core import Encoding
from langchain_core.runnables.base import RunnableSerializable

from core import settings


class GPTModelName(StrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"


@dataclass
class GPTModel:
    name: GPTModelName
    temperature: float
    max_input_tokens: int | None = None
    encoding: Encoding | None = None

    def __post_init__(self) -> None:
        self.encoding = tiktoken.encoding_for_model(self.name)

    @property
    def llm_instance(self) -> ChatOpenAI:
        return ChatOpenAI(model=self.name, temperature=self.temperature, api_key=settings.OPENAI_API_KEY)

    def invoke(self, text: str, runnable: RunnableSerializable | None = None) -> str:
        if runnable is not None:
            return runnable.invoke({"text": text}).content
        return self.llm_instance.invoke(text).content


GPT_MODELS = {
    "gpt-3.5-turbo": GPTModel(name=GPTModelName.GPT_3_5_TURBO, temperature=0.9, max_input_tokens=16385),
    "gpt-4o": GPTModel(name=GPTModelName.GPT_4O, temperature=0.9, max_input_tokens=128000),
    "gpt-4o-mini": GPTModel(name=GPTModelName.GPT_4O, temperature=0.9, max_input_tokens=128000),
}
