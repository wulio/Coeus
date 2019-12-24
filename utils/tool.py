# coding: utf-8
__author__ = 'deff'
import re


class Tools:
    @staticmethod
    def xml_assent(word):
        symbola = re.compile('>')
        word = symbola.sub('&lt;', word)
        symbolb = re.compile('<')
        word = symbolb.sub('&gt;', word)
        symbolc = re.compile('&')
        word = symbolc.sub('&amp;', word)
        symbold = re.compile('\'')
        word = symbold.sub('&apos;', word)
        symbole = re.compile('\"')
        word = symbole.sub('&quot;', word)
        return word
