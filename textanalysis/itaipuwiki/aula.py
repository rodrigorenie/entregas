import wikipedia
import string
import nltk
import os

from nltk.corpus import stopwords
from wordcloud import WordCloud


class Aula:
    """Classe que implementa as atividades da aula do dia 05/03.

    """

    def __init__(self):
        pass


def aula():

    def tokenizer(text, lang='portuguese'):
        sw = stopwords.words(lang)

        for c in string.punctuation:
            sw += [c]

        sw += ['de']

        text = nltk.sent_tokenize(text)
        text = [nltk.word_tokenize(s) for s in text]
        text = [[token for token in sent if token not in sw] for sent in text]
        return text

    # Get wiki content.
    wikipedia.set_lang('pt')
    wikicontent = wikipedia.page('Usina Hidrelétrica de Itaipu').content
    wikicontent = wikicontent.lower()

    # TODO
    # wikisummary = summarize(wikicontent, word_count=250)  # ratio=0.05)

    # palavras chave
    wikitokens = tokenizer(wikicontent)

    rs = nltk.RSLPStemmer()
    stem_text = [rs.stem(token) for sent in wikitokens for token in sent]
    key_words = ' '.join(stem_text)

    print(key_words)

    wordcloud = WordCloud(width=800, height=400,
                          relative_scaling=1.0).generate(key_words)

    dadospath = os.path.dirname(__file__) + '/../dados/'
    print(dadospath + '/g_wordcloud_wiki.png')
    wordcloud.to_file(dadospath + '/g_wordcloud_wiki.png')
