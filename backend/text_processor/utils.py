from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tiktoken.core import Encoding
from text_processor.consts import SUMMARIZING_PROMPT
from text_processor.schema import GPTModelName, GPT_MODELS, GPTModel


def num_tokens_from_string(string: str, encoding: Encoding) -> int:
    """Returns the number of tokens in a text string."""
    return len(encoding.encode(string))

def split_string_up_to_token_limit(
        text: str,
        model: GPTModel,
) -> list[str]:
    encoding = model.encoding
    if len(encoding.encode(text)) <= model.max_input_tokens:
        return [text]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name=model.name,
        chunk_size=model.max_input_tokens,
        chunk_overlap=0,
    )
    return text_splitter.split_text(text)


def summarize_text(text: str) -> str:
    # NOTE: we'll use gpt-4o-mini for such simple task as summarization, but you can choose any from popular models
    model = GPT_MODELS[GPTModelName.GPT_4O_MINI.value]
    prompt = PromptTemplate.from_template(SUMMARIZING_PROMPT)
    chain = prompt | model.llm_instance
    summarized = []
    # NOTE: although we take a single-paged pdf, we should make a check, that number of text's tokens is less than max_input_tokens
    if num_tokens_from_string(text, model.encoding) > model.max_input_tokens:
        for chunk in split_string_up_to_token_limit(text, model):
            summarized.append(model.invoke(chunk, runnable=chain))
    else:
        summarized = [model.invoke(text, runnable=chain)]
    print('summarized: ', summarized)

    return '\n\n'.join(summarized)
