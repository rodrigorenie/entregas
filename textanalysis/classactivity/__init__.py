import os
import nltk

from textanalysis.classactivity.classactivity import News

nltk_data = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'nltk')
nltk.data.path.append(nltk_data)

__all__ = ['News']
