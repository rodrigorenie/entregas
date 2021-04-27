from textanalysis.classactivity import News

if __name__ == '__main__':
    c = News()
    for word, top in c.top_words():
        print(word, top)
    for b, top in c.top_bigram():
        print(b, top)
    print(list(c.sents_pos))
    # for tree in c.sents_ner:
    #     print(type(tree))

