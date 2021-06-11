import nltk
import dsutils

from textanalysis.classactivity.classactivity import News

nltk.data.path.append(dsutils.datadir.join('nltk'))

__all__ = ['News']
