import argparse
from pathlib import Path

import frontmatter
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain

from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add keywords to blog posts")
    parser.add_argument("dir_posts", type=str, help="Directory with markdown posts")
    args = parser.parse_args()

    PATH_POSTS = args.dir_posts

    file_paths = []
    for path in Path(PATH_POSTS).rglob('*.md'):
        if not path.name == "_index.md": 
            file_paths.append(path)

    # see https://stackoverflow.com/questions/761824/python-how-to-convert-markdown-formatted-text-to-text/76934168#76934168
    markdown_parser = MarkdownIt(renderer_cls=RendererPlain)

    kw_model = KeyBERT()
    # see https://maartengr.github.io/KeyBERT/guides/countvectorizer.html#usage
    vectorizer = KeyphraseCountVectorizer(spacy_pipeline='de_core_news_sm', pos_pattern='<N.*>')
    for path in file_paths:
        with path.open() as f:
            metadata, content = frontmatter.parse(f.read())
            txt_data = markdown_parser.render(content)

            keywords = kw_model.extract_keywords(txt_data, vectorizer=vectorizer)
            print(metadata["date"], metadata["title"], keywords)




