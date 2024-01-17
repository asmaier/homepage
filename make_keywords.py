import argparse
import shutil
from pathlib import Path, PurePath
from collections import Counter
import statistics

import frontmatter
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp

import langdetect

n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 2048    # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
n_ctx = 14336     # Our context size in tokens


llm = LlamaCpp(
    model_path="./models/mistral-7b-openorca.Q5_K_M.gguf",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=n_ctx,
    temperature=0.0,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    # callback_manager=callback_manager,
    # verbose=True,  # Verbose is required to pass to the callback manager
    grammar_path="./list.gbnf"
)
# see https://github.com/ggerganov/llama.cpp/issues/999
llm.client.verbose = False

template = """
Ich habe das folgende Dokument:

'''
{document}
'''

Gib mir als Pythonliste die fünf Kategorien aus Wikipedia die am besten zu dem Dokument passen.
Eine Kategorie darf das Wort "Kategorie" nicht enthalten.
Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.

kategorien =
"""

prompt = PromptTemplate(template=template, input_variables=["document"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


def extract_topics(text):
    # We assume here that one token is one character.
    # Usually one token has more than one character.
    # But assuming one token = one char will always work
    MAX_SIZE = 1 * n_ctx
    cutoff = len(text) if len(text) < MAX_SIZE else MAX_SIZE
    result = llm_chain.invoke({"document": text[:cutoff]})
    # Using eval is unsave and might lead to code injections .
    # But we use it here, because we assume we can trust our own documents.
    return eval(result["text"])


def update_metadata(post, taxonomy, keywords):
    # update existing keywords (and lowercase them)
    old_keywords = []
    if taxonomy in post:
        old_keywords = [kw.lower() for kw in post[taxonomy]]
    new_keywords = [kw.lower() for kw in keywords]
    updated_keywords = set(old_keywords) | set(new_keywords)
    post[taxonomy] = list(updated_keywords)

    print(i, post["date"], post["title"], old_keywords, "->", post[taxonomy])
    return post


def set_metadata(post, taxonomy, value):

    old_value = None
    if taxonomy in post:
        old_value = post[taxonomy]
    post[taxonomy] = value

    print(i, post["date"], post["title"], old_value, "->", post[taxonomy])
    return post


def extract_languages(txt_data):
    if len(txt_data) == 0:
        return "empty"

    langcodes = {"en": "english", "de": "deutsch", "ru": "русский"}

    try:
        result = langdetect.detect(txt_data)
        if result in langcodes:
            return langcodes[result]
        else:
            return "unknown"
    except langdetect.lang_detect_exception.LangDetectException as err:
        return "empty"



def extract_date(post):

    if "date" in post:
        if isinstance(post["date"], str):
            return post["date"][:4]
        else:
            return post["date"].year


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add keywords to blog posts")
    parser.add_argument("dir_posts", type=str, help="Directory with markdown posts")
    parser.add_argument("--real-run", action="store_true", help="Do persist the changes")
    args = parser.parse_args()

    PATH_POSTS = args.dir_posts

    file_paths = []
    for path in Path(PATH_POSTS).rglob('*.md'):
        if not path.name == "_index.md": 
            file_paths.append(path)

    # see https://stackoverflow.com/questions/761824/python-how-to-convert-markdown-formatted-text-to-text/76934168#76934168
    markdown_parser = MarkdownIt(renderer_cls=RendererPlain)

    docs = []
    keywords = []
    for i, path in enumerate(file_paths[200:210]):
        with path.open("rb") as src_file:
            # create backup files path
            backup_path = path.with_suffix(".bak")

            # Prevent overwriting existing backup files
            if backup_path.exists():
                print(f"Skipping backup as {backup_path} already exists")
            else:
                if args.real_run:
                    with backup_path.open("wb") as dest_file:
                        shutil.copyfileobj(src_file, dest_file)

        with path.open("rb+") as f:
            post = frontmatter.loads(f.read())
            txt_data = markdown_parser.render(post.content)

            # Assuming the following date format YYYY-MM-DD
            year = extract_date(post)
            post = set_metadata(post, "year", year)

            languages = extract_languages(txt_data)
            post = update_metadata(post, "languages", [languages])

            topics = extract_topics(txt_data)
            post = update_metadata(post, "tags", topics)

            if args.real_run:
                # reset file pointer to beginning of file
                f.seek(0)
                frontmatter.dump(post, f, sort_keys=False)



