import docx
import nltk
import string

from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import ngrams
from nltk import tokenize
from nltk.corpus import webtext
from nltk.corpus import stopwords
from nltk.corpus import machado


def ex01():
    # Rodrigo Renie de Braga Pinto
    # TEXT ANALYSIS(Apostila)Parte 1.docx
    # Exercitando 1
    # Execute o que se pede.
    # Imprima as palavras dos documentos neg/cv002_tok-3321.txt e
    # pos/cv003_tok-8338.txt
    corpus_reader = CategorizedPlaintextCorpusReader(
        'dados/mix20_rand700_tokens_cleaned/tokens/',
        '.*.txt', cat_pattern=r'(\w+)/*')

    words = {
        'neg/cv002_tok-3321.txt': [],
        'pos/cv003_tok-8338.txt': []
    }

    for file in words:
        words[file] = corpus_reader.words(fileids=file)
        print('Palavras no arquivo {}: {}'.format(file, words[file]))


def ex02():
    # Rodrigo Renie de Braga Pinto
    # TEXT ANALYSIS(Apostila)Parte 1.docx
    # Exercitando 2
    # Execute o que se pede.
    # Utilize o arquivo Noticia_1 disponível na pasta de dados da turma e liste os
    # 50 bigramas e trigramas mais frequentes obtidos do texto.
    docpath = 'dados/Noticia_1.docx'
    doc = docx.Document(docpath)

    words = [w for p in doc._paragraphs for w in p.text.split()]

    fb2 = nltk.FreqDist(ngrams(words, 2))
    fb3 = nltk.FreqDist(ngrams(words, 3))

    print('{:2} {:>30s} : {:4} {:>40s} : {:4}'.format(
        ' ', 'Bigrama', 'Freq', 'Trigrama', 'Freq'))

    for i, ((bw, bf), (tw, tf)) in enumerate(zip(fb2.most_common(50),
                                                 fb3.most_common(50))):
        print('{:02} {:>30s} : {:<4} {:>40s} : {:<4}'.format(i + 1, str(bw), bf,
                                                             str(tw), tf))


def ex03():
    # Rodrigo Renie de Braga Pinto
    # TEXT ANALYSIS(Apostila)Parte 1.docx
    # Exercitando 3
    # Execute o que se pede.
    # Analise a frequência das palavras ['the', 'that'] no arquivo singles.txt e,
    # depois, no arquivo pirates.txt.
    # Inclua a geração do gráfico de frequência.
    # Gere a lista dos 15 bigramas mais frequentes do texto.
    # Gere a lista dos 20 quadrigramas gramas mais frequentes que possuam a
    # palavra 'life'
    data = {
        'singles.txt': {
            'tokens': [],
            'freq_tokens': None,
            'freq_tokens_top15': [],
            'freq_bigrams': None,
            'freq_bigrams_top15': [],
            'freq_quadrigrams_life': []
        },
        'pirates.txt': {
            'tokens': [],
            'freq_tokens': None,
            'freq_tokens_top15': [],
            'freq_bigrams': None,
            'freq_bigrams_top15': [],
            'freq_quadrigrams_life': []
        }
    }

    # Gera os stopwords e inclui palavras personalizadas
    sw = stopwords.words('english') + [
        "[", "]", ".", ",", "?", "*", ":", "...", "!", "'", "'s",
        "#", "(", ")", "'m", "-", "'ve", "ft.", "n't", "y.o", "&", "..",
        "n/s", "s/d", "n/d", "s/s", "s/e", "''"
    ]

    for file in data:
        text = webtext.raw(file)

        # Gera e filtra os tokens de cada arquivo
        data[file]['tokens'] = tokenize.word_tokenize(text)
        data[file]['tokens'] = [t.lower() for t in data[file]['tokens']
                                if t.lower() not in sw]

        # Gera os dados de frequência dos tokens
        data[file]['freq_tokens'] = nltk.FreqDist(data[file]['tokens'])

        # Gera os dados dos 15 tokens mais frequentes
        top15 = data[file]['freq_tokens'].most_common(15)
        data[file]['freq_tokens_top15'] = top15

        # Gera os dados de frequência dos bigramas
        bigram = ngrams(data[file]['tokens'], 2)
        data[file]['freq_bigrams'] = nltk.FreqDist(bigram)

        # Gera os dados dos 15 bigramas mais frequentes
        top15 = data[file]['freq_bigrams'].most_common(15)
        data[file]['freq_bigrams_top15'] = top15

        # Gera os dados de frequência dos quadrigramas com palavra "life"
        quadrigram = [ng for ng in ngrams(data[file]['tokens'], 4) if 'life' in ng]
        data[file]['freq_quadrigrams_life'] = nltk.FreqDist(quadrigram)

        # Imprime frequência das palavras 'the' e 'that'
        print('\n{:20s} {:35s} {}'.format('Arquivo', 'Token', 'Frequência'))
        for word in ['the', 'that']:
            freq = data[file]['freq_tokens'][word]
            print('{:20s} {:35s} {:03}'.format(file, word, freq))

        # Imprime Top 15 Tokens
        print('\n{:20s} {:35s} {}'.format('Arquivo', 'Top 15 Tokens', 'Frequência'))
        for token, freq in data[file]['freq_tokens_top15']:
            print('{:20s} {:35s} {:03}'.format(file, token, freq))

        # Imprime Top 15 Bigramas
        print('\n{:20s} {:35s} {}'.format(
            'Arquivo', 'Top 15 Bigrama', 'Frequência'))
        for bigram, freq in data[file]['freq_bigrams_top15']:
            print('{:20s} {:35s} {:03}'.format(file, str(bigram), freq))

        # Imprime Top 20 Quadrigramas com palavra "life"
        print('\n{:20s} {:50s} {}'.format(
            'Arquivo', 'Top 20 Quadrigrama', 'Frequência'))
        top20 = data[file]['freq_quadrigrams_life'].most_common(20)
        for quadrigram, freq in top20:
            print('{:20s} {:50s} {:03}'.format(file, str(quadrigram), freq))

    data['singles.txt']['freq_tokens'].plot(cumulative=False)
    data['pirates.txt']['freq_tokens'].plot(cumulative=True)


def ex04():
    # Rodrigo Renie de Braga Pinto
    # TEXT ANALYSIS(Apostila)Parte 1.docx
    # Exercitando 4
    # Execute o que se pede.

    # Execute print(machado.readme()) para conhecer melhor o corpus
    print(machado.readme())

    # Utilizando o corpus machado, elabore um programa que atenda aos requisitos:

    # a. Quais são as categorias presentes no corpus?
    print('Categorias: {}'.format(machado.categories()))

    # b. Quais são os documentos dentro desse corpus?
    print('Documentos: {}'.format(machado.fileids()))

    # c. Imprima o conteúdo do arquivo do documento que contem a obra
    #    Memórias Postumas de Braz Cubas
    book_fileid = 'romance/marm05.txt'
    print(machado.raw(book_fileid))

    # d. Analise a frequência das palavras [‘olhos’,’estado’] em
    #    Memórias Postumas de Bras Cubas
    book_text = machado.raw(book_fileid)
    book_tokens = tokenize.word_tokenize(book_text)
    book_freq = nltk.FreqDist(book_tokens)

    for w in ['olhos', 'estado']:
        print('Frequência da palavra {:>8s} : {:03}'.format(w, book_freq[w]))

    # e. Quantas palavras há no texto? Use len(texto)
    print('Total de palavras: {}'.format(len(book_text)))

    # f. Quantas palavras distintas há na obra?
    print('Total de palavras distintas: {}'.format(len(book_freq)))

    # g. Qual é o vocabulário (palavras) presentes na obra?
    print('Vocabulário: {}'.format(book_freq.keys()))

    # h. Quais são os 15 termos mais repetidos no texto de Machado de Assis?
    print('\n{:25s} {}'.format('Top 15', 'Frequência'))
    for w, f in book_freq.most_common(15):
        print('{:25s} {:03}'.format(w, f))

    # i. Tabular a frequência de palavras
    print('\n')
    book_freq.tabulate(15, cumulative=False)

    # j. Gerar um gráfico com os 15 termos mais repetidos
    book_freq.plot(15, title='Top 15 words', cumulative=False)

    # k. Remova os termos indesejados  e repita as questões 'h' a 'j'
    book_stopwords = stopwords.words('portuguese')
    book_stopwords += ['\x97', '...', 'd.']
    book_stopwords += [p for p in string.punctuation]
    book_tokens = [t.lower() for t in book_tokens
                   if t.lower() not in book_stopwords]
    book_freq = nltk.FreqDist(book_tokens)

    print('\n{:25s} {}'.format('Top 15', 'Frequência'))
    for w, f in book_freq.most_common(15):
        print('{:25s} {:03}'.format(w, f))

    print('\n')
    book_freq.tabulate(15, cumulative=False)

    book_freq.plot(15, title='Top 15 words', cumulative=False)

    # l. Obter a lista de todos os trigramas do texto
    for trigram in ngrams(book_tokens, 3):
        print('{:35s}'.format(str(trigram)))

    # m. Obter a lista dos 15 bigramas que contenham a palavra 'olhos'
    olhos_bigram = [ng for ng in ngrams(book_tokens, 2) if 'olhos' in ng]
    olhos_freq = nltk.FreqDist(olhos_bigram)
    print('\n{:30s} {}'.format('Top 15 Olhos', 'Frequência'))
    for b, f in olhos_freq.most_common(15):
        print('{:30s} {:03}'.format(str(b), f))

    # n. Gerar o gráfico dos bigramas com a palavra 'olhos'
    olhos_freq.plot(15, cumulative=True)
