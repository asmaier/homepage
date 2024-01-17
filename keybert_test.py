import argparse
from pathlib import Path
from collections import Counter
import statistics

import frontmatter
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain

from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer, KeyphraseTfidfVectorizer

from bertopic import BERTopic

import yake
import pytextrank
import spacy
## Don't forget to install the model first:
# $ python -m spacy download de_core_news_sm
# see https://spacy.io/models/de

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


    kw_extractor = yake.KeywordExtractor(top=5, n=1, lan="de")
    kw_model = KeyBERT()
    # see https://maartengr.github.io/KeyBERT/guides/countvectorizer.html#usage

    vectorizer = KeyphraseCountVectorizer(spacy_pipeline='de_core_news_sm', pos_pattern='<N.*>', stop_words='german')
    # vectorizer = KeyphraseTfidfVectorizer(spacy_pipeline='de_core_news_sm', pos_pattern='<N.*>')

    nlp = spacy.load("de_core_news_sm")
    # nlp.add_pipe("topicrank")

    # print(nlp.pipe_names)

    docs = []
    keywords = []
    for path in file_paths[:100]:
        with path.open() as f:
            metadata, content = frontmatter.parse(f.read())
            txt_data = markdown_parser.render(content)
            result = nlp(txt_data)
            text = ' '.join([x.lemma_ for x in result])
            docs.append(text)
            # keywords_for_doc = kw_extractor.extract_keywords(txt_data)
            keywords_for_doc = kw_model.extract_keywords(text, top_n=5, vectorizer=vectorizer)

            # result = nlp(txt_data)
            # keywords_for_doc = [(phrase.text, phrase.rank) for phrase in result._.phrases[:5]]

            keywords.append(keywords_for_doc)
            print(metadata["date"], metadata["title"], keywords_for_doc)

    # keywords = kw_model.extract_keywords(docs, top_n=5)

    words = []
    for element in keywords:
        for entry in element:
            words.append(entry[0].lower())

    word_counter = Counter(words)
    most_common = word_counter.most_common(20)  # get the top 20 most
    print(len(most_common))
    print(most_common)

    filtered_words = [word for word, count in word_counter.items() if count > 2]
    print(len(filtered_words))
    print(filtered_words)

    set_of_words = set(words)  # remove duplicates

    word_lengths = [len(word) for word in set_of_words]
    average = statistics.mean(word_lengths)
    median = statistics.median(word_lengths)

    print("Total number of words:", len(set_of_words))
    print("Average word length:", average)
    print("Median word length:", median)

    sorted_words = sorted(set_of_words)
    print(sorted_words)

    # print(keywords)        
            
    #print(metadata["date"], metadata["title"], keywords)

    # vectorizer = KeyphraseCountVectorizer(spacy_pipeline='de_core_news_md', pos_pattern='<N.*>', stop_words='german')
    # topic_model = BERTopic(language="multilingual", vectorizer_model=vectorizer, min_topic_size=2)
  

    # topics, probs = topic_model.fit_transform(docs)
    # print(topic_model.get_topic_info())
    # fig1 = topic_model.visualize_heatmap()
    # fig2 = topic_model.visualize_topics()

    # fig1.write_html("heatmap.html")  
    # fig2.write_html("topics.html")


    # Total number of words: 430
    # Average word length: 9.402325581395349
    # Median word length: 8.
    # [('regierung', 8), ('deutschland', 7), ('berlin', 6), ('russland', 5), ('submitting', 4), ('security', 4), ('block', 4), ('werbung', 3), ('cloudflar', 3), ('wirtschaft', 3), ('soviet', 3), ('facebook', 3), ('internet', 3), ('ukraine', 3), ('putin', 3), ('euro', 2), ('jahr', 2), ('türkei', 2), ('bundesregierung', 2), ('bundesland', 2)]



            



