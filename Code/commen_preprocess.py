from __future__ import absolute_import, division
import sys, os, re, csv, codecs, numpy as np, pandas as pd
import re
import wordninja as wn
from nltk.tokenize import TweetTokenizer
tokenizer=TweetTokenizer()
from nltk.corpus import stopwords
import emoji
stop_words = set(stopwords.words("english"))


def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    
    if hashtag_body.isupper():
        result = u"hashtag {} allcaps".format(hashtag_body)
    else:
        for word in no_abbre.keys():
            hashtag_body=hashtag_body.replace(word,no_abbre[word])

        word_list=wn.split(hashtag_body)
        hashtag_body=' '.join(word for word in word_list)
        result = u"hashtag {} ".format(hashtag_body)
    return result


def substitute_repeats_fixed_len(text, nchars, ntimes=3):
     return re.sub(r"(\S{{{}}})(\1{{{},}})".format(nchars, ntimes-1), r"\1", text)

def substitute_repeats(text, ntimes=3):
        # Truncate consecutive repeats of short strings
        for nchars in range(1, 20):
            text = substitute_repeats_fixed_len(text, nchars, ntimes)
        return text
def subs(text):
    text = text.group()
    return text[1:len(text)-1]



    
FLAGS = re.MULTILINE | re.DOTALL

def clean_english(text, for_embeddings=False,remove_stopwords=False, remove_punctuations=False):
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text)
    
    text=emoji.demojize(text)
    text= re.sub(r":\w+:",subs, text)    
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "website")

    for word in no_abbre.keys():
        text=text.replace(word,no_abbre[word])

    if for_embeddings:
        text = re_sub(r"@\w+", "user")
    else:
        text = text.replace('@', '')
    
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "number")
    
    
    words=tokenizer.tokenize(text)

    if remove_stopwords:
        words = [w for w in words if not w in stop_words]
    
    text=" ".join(words)
    
    # Remove some special characters, or noise charater, but do not remove all!!
    if remove_punctuations:
        text = re.sub(r'([\.\'\"\/\-\_\--\_])',' ', text)
    else:
        text = re.sub(r'([\.\'\"\/\-\_\-\_\(\)\{\}])',' ', text)
    clean_sent= re.sub(r'([\;\|•«\n])',' ', text)
    
    FLAG_remove_non_ascii =False
    if FLAG_remove_non_ascii:
        return clean_sent.encode("ascii", errors="ignore").decode().strip().lower()
    else:
        return clean_sent.strip().lower()
      
def clean_hindi(text, for_embeddings=False,remove_stopwords=False, remove_punctuations=False):
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text)
    
    text= re.sub(r":\w+:",subs, text)    
    text=  emoji.demojize(text)
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "website")

    
    if for_embeddings:
        text = re_sub(r"@\w+", "user")
    else:
        text = text.replace('@', '') 
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "number")
    
    
    
    
    # Remove some special characters, or noise charater, but do not remove all!!
    if remove_punctuations:
        text = re.sub(r'([\.\'\"\/\-\_\--\_])',' ', text)
    else:
        
    clean_sent= re.sub(r'([\;\|•«\n])',' ', text)
    
    FLAG_remove_non_ascii =False
    if FLAG_remove_non_ascii:
        return clean_sent.encode("ascii", errors="ignore").decode().strip().lower()
    else:
        return clean_sent.strip()










print(clean_english("#brexit #rapefugee"))