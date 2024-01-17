import argparse
import re
from collections import Counter
from pathlib import Path
import statistics

import frontmatter
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 2048  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="./models/mistral-7b-openorca.Q5_K_M.gguf",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=16384,
    temperature=0.0,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    # callback_manager=callback_manager,
    # verbose=True,  # Verbose is required to pass to the callback manager
    grammar_path="./list.gbnf"
)
# see https://github.com/ggerganov/llama.cpp/issues/999
llm.client.verbose = False

# # Total number of words: 54
# # Average word length: 11.518518518518519
# # Median word length: 11.0
# # Total number of words: 525
# # Average word length: 11.862857142857143
# # Median word length: 11
# # [('russland', 8), ('berlin', 5), ('facebook', 3), ('deutschland', 3), ('datenschutz', 3), ('signal', 3), ('regierung', 3), ('corona', 2), ('türkei', 2), ('transparenz', 2), ('korruption', 2), ('solar', 2), ('fsb', 2), ('bvg', 2), ('internet', 2), ('amerikaner', 2), ('wissenschaft', 2), ('zensur', 2), ('ärzte', 2), ('probleme', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten Schlagworte die das Dokument beschreiben.
# Ein Schlagwort soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Schlagworte und keinen anderen Text davor oder danach.
#
# schlagworte =
# """

# # Total number of words: 63
# # Average word length: 11.317460317460318
# # Median word length: 11
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten Stichworte die das Dokument beschreiben.
# Ein Stichwort soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Stichworte und keinen anderen Text davor oder danach.
#
# stichworte =
# """

# # Total number of words: 55
# # Average word length: 10.909090909090908
# # Median word length: 11
# # Total number of words: 669
# # Average word length: 12.059790732436472
# # Median word length: 10
# # [('berlin', 8), ('russland', 8), ('deutschland', 3), ('signal', 3), ('gesetze', 3), ('werbung', 2), ('corona', 2), ('türkei', 2), ('china', 2), ('transparenz', 2), ('fsb', 2), ('bundesrepublik', 2), ('polizei', 2), ('richter', 2), ('amerikaner', 2), ('regierung', 2), ('ärzte', 2), ('probleme', 2), ('nicht', 2), ('grundgesetz', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten Lemmas die das Dokument beschreiben.
# Ein Lemma soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Lemmas und keinen anderen Text davor oder danach.
#
# lemmas =
# """

# # Total number of words: 53
# # Average word length: 12.415094339622641
# # Median word length: 10
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten Themen die das Dokument beschreiben.
# Ein Thema soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Themen und keinen anderen Text davor oder danach.
#
# themen =
# """

# # Total number of words: 53
# # Average word length: 11.018867924528301
# # Median word length: 10
#
# Total number of words: 564
# Average word length: 13.03368794326241
# Median word length: 11.0
# [('russland', 5), ('deutschland', 4), ('datenschutz', 4), ('internet', 3), ('berlin', 3), ('video', 2), ('corona', 2), ('türkei', 2), ('transparenz', 2), ('korruption', 2), ('wirtschaft', 2), ('bürokratie', 2), ('latex', 2), ('cloudflare', 2), ('werbung', 2), ('fsb', 2), ('bvg', 2), ('deutsche', 2), ('zensur', 2), ('signal', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten übergeordneten Themen die das Dokument beschreiben.
# Ein Thema soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Themen und keinen anderen Text davor oder danach.
#
# themen =
# """

# # Total number of words: 56
# # Average word length: 11.964285714285714
# # Median word length: 11.0
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten übergeordneten Schlagworte die das Dokument beschreiben.
# Ein Schlagwort soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Schlagworte und keinen anderen Text davor oder danach.
#
# schlagworte =
# """

# # Total number of words: 53
# # Average word length: 11.415094339622641
# # Median word length: 11
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten Kategorien die das Dokument beschreiben.
# Eine Kategorie soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.
#
# kategorien =
# """

# # Total number of words: 55
# # Average word length: 10.636363636363637
# # Median word length: 10
#
# # Total number of words: 445
# # Average word length: 11.501123595505618
# # Median word length: 10
# # [('russland', 10), ('politik', 8), ('deutschland', 6), ('wirtschaft', 5), ('umwelt', 5), ('berlin', 5), ('datenschutz', 5), ('regierung', 4), ('ukraine', 4), ('facebook', 3), ('politics', 3), ('europa', 3), ('klimawandel', 3), ('initiative', 2), ('corona', 2), ('türkei', 2), ('transparenz', 2), ('finanzen', 2), ('technologie', 2), ('humor', 2)]
template = """
Ich habe das folgende Dokument:

'''
{document}
'''

Gib mir als Pythonliste die fünf wichtigsten übergeordneten Kategorien zu denen das Dokument gehört.
Eine Kategorie soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.

kategorien =
"""

# # Total number of words: 80
# # Average word length: 10.35
# # Median word length: 10.0
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf wichtigsten übergeordneten Lemmas die das Dokument beschreiben.
# Ein Lemma soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Lemmas und keinen anderen Text davor oder danach.
#
# lemmas =
# """

# # Total number of words: 440
# # Average word length: 13.027272727272727
# # Median word length: 12.0
# # [('politik', 9), ('deutschland', 9), ('russland', 9), ('umwelt', 7), ('datenschutz', 6), ('wirtschaft', 5), ('berlin', 5), ('internet', 4), ('klimawandel', 4), ('facebook', 3), ('latex', 3), ('künstliche intelligenz', 3), ('psychologie', 3), ('technologie', 3), ('initiative', 2), ('schweiz', 2), ('werbung', 2), ('transparenz', 2), ('business', 2), ('website', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf Kategorien aus Wikipedia die am besten zu dem Dokument passen.
# Eine Kategorie soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.
#
# kategorien =
# """
# # Total number of words: 481
# # Average word length: 12.353430353430353
# # Median word length: 11
# # [('politik', 13), ('deutschland', 10), ('russland', 9), ('umwelt', 6), ('datenschutz', 6), ('website', 4), ('berlin', 4), ('software', 3), ('wirtschaft', 3), ('internet', 3), ('sicherheit', 3), ('europa', 3), ('steuern', 3), ('psychologie', 3), ('technologie', 3), ('klimawandel', 3), ('reichtum', 3), ('schweiz', 2), ('apple', 2), ('werbung', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf Kategorien aus Wikipedia die am besten zu dem Dokument passen.
# Eine Kategorie soll aus einem einzelnen Wort ohne Sonderzeichen bestehen.
# Eine Kategorie darf das Wort "Kategorie" nicht enthalten.
# Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.
#
# kategorien =
# """

# # Total number of words: 409
# # Average word length: 13.88997555012225
# # Median word length: 13
# # [('politik', 13), ('russland', 11), ('deutschland', 8), ('', 8), ('datenschutz', 7), ('umwelt', 6), ('wirtschaft', 4), ('klimawandel', 4), ('latex', 3), ('europäische union', 3), ('steuern', 3), ('psychologie', 3), ('medizin', 3), ('kategorie 1', 3), ('kategorie 3', 3), ('kategorie 4', 3), ('kategorie 5', 3), ('einkommen', 2), ('apple inc', 2), ('pandemie', 2)]
# template = """
# Ich habe das folgende Dokument:
#
# '''
# {document}
# '''
#
# Gib mir als Pythonliste die fünf Kategorien aus Wikipedia die am besten zu dem Dokument passen.
# Gib mir nur die Liste der Kategorien und keinen anderen Text davor oder danach.
#
# kategorien =
# """

# Total number of words: 46
# Average word length: 12.08695652173913
# Median word length: 11.0

# Total number of words: 472
# Average word length: 13.315677966101696
# Median word length: 12.0
# [('politik', 17), ('russland', 12), ('deutschland', 10), ('umwelt', 7), ('datenschutz', 6), ('wirtschaft', 5), ('europäische union', 5), ('psychologie', 4), ('mathematik', 3), ('physik', 3), ('internet', 3), ('steuern', 3), ('medizin', 3), ('klimawandel', 3), ('berlin', 3), ('apple inc', 2), ('verkehr', 2), ('künstliche intelligenz', 2), ('energieversorgung', 2), ('emacs', 2)]

# Total number of words: 4541
# Average word length: 14.644131248623651
# Median word length: 14
# [('politik', 245), ('deutschland', 165), ('russland', 136), ('berlin', 82), ('datenschutz', 56), ('klimawandel', 55), ('umwelt', 53), ('wirtschaft', 49), ('internet', 49), ('soziale medien', 38), ('wissenschaft', 38), ('physik', 37), ('technologie', 37), ('medien', 36), ('europäische union', 35), ('youtube', 34), ('coronavirus', 34), ('pandemie', 32), ('ukraine', 32), ('medizin', 26)]

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

# pattern = r'\[(.*?)\]'

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

    docs = []
    keywords = []
    for i, path in enumerate(file_paths[:10]):
        with path.open() as f:
            metadata, content = frontmatter.parse(f.read())
            txt_data = markdown_parser.render(content)
            # print(i, metadata["date"], metadata["title"])

            MAX_SIZE = 16384
            cutoff = len(txt_data) if len(txt_data) < MAX_SIZE else MAX_SIZE

            result = llm_chain.invoke({"document": txt_data[:cutoff]})

            keywords_for_doc = eval(result["text"])

            # match = re.search(pattern, result["text"], re.DOTALL)
            # if match:
            #    keywords_for_doc = eval(match.group(1).replace("\n", ""))

            keywords.append(keywords_for_doc)
            print(i, metadata["date"], metadata["title"], keywords_for_doc)
            # else:
            #    print(metadata["date"], metadata["title"], "No keywords found in ", result["text"])

    # keywords = kw_model.extract_keywords(docs, top_n=5)

    words = []
    for element in keywords:
        for entry in element:
            words.append(entry.lower())

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
