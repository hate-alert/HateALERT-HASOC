from __future__ import absolute_import, division
import sys, os, re, csv, codecs, numpy as np, pandas as pd
import re
import wordninja as wn
from nltk.tokenize import TweetTokenizer
tokenizer=TweetTokenizer()
from nltk.corpus import stopwords
import emoji
stop_words = set(stopwords.words("english"))

no_abbre = {
"ain't" : "have not",
"aren't" : "are not",
"can't" : "cannot",
"couldn't" : "could not",
"didn't" : "did not",
"doesn't" : "does not",
"don't" : "do not",
"hadn't" : "had not",
"hasn't" : "has not",
"haven't" : "have not",
"he'd" : "he would",
"he'll" : "he will",
"he's" : "he is",
"i'd" : "I would",
"i'd" : "I had",
"i'll" : "I will",
"i'm" : "I am",
"isn't" : "is not",
"it's" : "it is",
"it'll":"it will",
"i've" : "I have",
"let's" : "let us",
"mightn't" : "might not",
"mustn't" : "must not",
"shan't" : "shall not",
"she'd" : "she would",
"she'll" : "she will",
"she's" : "she is",
"shouldn't" : "should not",
"that's" : "that is",
"there's" : "there is",
"they'd" : "they would",
"they'll" : "they will",
"they're" : "they are",
"they've" : "they have",
"we'd" : "we would",
"we're" : "we are",
"weren't" : "were not",
"we've" : "we have",
"what'll" : "what will",
"what're" : "what are",
"what's" : "what is",
"what've" : "what have",
"where's" : "where is",
"who'd" : "who would",
"who'll" : "who will",
"who're" : "who are",
"who's" : "who is",
"who've" : "who have",
"won't" : "will not",
"wouldn't" : "would not",
"you'd" : "you would",
"you'll" : "you will",
"you're" : "you are",
"you've" : "you have",
"'re": " are",
"wasn't": "was not",
"we'll":" will",
"didn't": "did not",
"tryin'":"trying",
"pls":"please",
"youre":"you are",
"DACA":" daca",
"brexit":"britain exit",
"wtf":"what the fuck",
"fingermiddle":"fuck",
"rapefugee":"rape refugee"
    
}



emojis = {
    "&lt;3": " good ",
    ":d": " good ",
    ":dd": " good ",
    ":p": " good ",
    "8)": " good ",
    ":-)": " good ",
    ":)": " good ",
    ";)": " good ",
    "(-:": " good ",
    "(:": " good ",
    "yay!": " good ",
    "yay": " good ",
    "yaay": " good ",
    "yaaay": " good ",
    "yaaaay": " good ",
    "yaaaaay": " good ",
    ":/": " bad ",
    ":&gt;": " sad ",
    ":')": " sad ",
    ":-(": " bad ",
    ":(": " bad ",
    ":s": " bad ",
    ":-s": " bad ",
    "&lt;3": " heart ",
    ":d": " smile ",
    ":p": " smile ",
    ":dd": " smile ",
    "8)": " smile ",
    ":-)": " smile ",
    ":)": " smile ",
    ";)": " smile ",
    "(-:": " smile ",
    "(:": " smile ",
    ":/": " worry ",
    ":&gt;": " angry ",
    ":')": " sad ",
    ":-(": " sad ",
    ":(": " sad ",
    ":s": " sad ",
    ":-s": " sad ",
    r"\br\b": "are",
    r"\bu\b": "you",
    r"\bhaha\b": "ha",
    r"\bhahaha\b": "ha"}

print(".....start_cleaning.........")



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
    
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can\'t", "can not", text)

    # general
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)
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
    #text = text.replace('_', ' ')
    #text = text.replace('-', ' ')
    
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
    
    text=emoji.demojize(text)
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "website")

    
    if for_embeddings:
        text = re_sub(r"@\w+", "user")
    else:
        text = text.replace('@', '')
    #text = text.replace('_', ' ')
    #text = text.replace('-', ' ')
    
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "number")
    
    
    
    
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










print(clean_english("#brexit #rapefugee"))









"""
from __future__ import absolute_import, division
import sys, os, re, csv, codecs, numpy as np, pandas as pd
import re


from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english') 



def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\-|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    vTEXT = re.sub(r'(www)(\w|\.|\-|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT.lower())


no_abbre = {
"ain't" : "have not",
"aren't" : "are not",
"can't" : "cannot",
"couldn't" : "could not",
"didn't" : "did not",
"doesn't" : "does not",
"don't" : "do not",
"hadn't" : "had not",
"hasn't" : "has not",
"haven't" : "have not",
"he'd" : "he would",
"he'll" : "he will",
"he's" : "he is",
"i'd" : "I would",
"i'd" : "I had",
"i'll" : "I will",
"i'm" : "I am",
"isn't" : "is not",
"it's" : "it is",
"it'll":"it will",
"i've" : "I have",
"let's" : "let us",
"mightn't" : "might not",
"mustn't" : "must not",
"shan't" : "shall not",
"she'd" : "she would",
"she'll" : "she will",
"she's" : "she is",
"shouldn't" : "should not",
"that's" : "that is",
"there's" : "there is",
"they'd" : "they would",
"they'll" : "they will",
"they're" : "they are",
"they've" : "they have",
"we'd" : "we would",
"we're" : "we are",
"weren't" : "were not",
"we've" : "we have",
"what'll" : "what will",
"what're" : "what are",
"what's" : "what is",
"what've" : "what have",
"where's" : "where is",
"who'd" : "who would",
"who'll" : "who will",
"who're" : "who are",
"who's" : "who is",
"who've" : "who have",
"won't" : "will not",
"wouldn't" : "would not",
"you'd" : "you would",
"you'll" : "you will",
"you're" : "you are",
"you've" : "you have",
"'re": " are",
"wasn't": "was not",
"we'll":" will",
"didn't": "did not",
"tryin'":"trying",
"ye": "you",
"stfu": "shut the fuck up",
"idubzz": "cancer",
"ho": "hoe",
"im": "i am",
"dm": "direct message",
"doesnt": "does not",
"its": "it is",
"lolol": "laugh out loud",
"lol": "laugh out loud",   
"lil":"little",
"y'all":"you all",
"rapefugee":"rape refugee"
}



emoji = {
    "&lt;3": " good ",
    ":d": " good ",
    ":dd": " good ",
    ":p": " good ",
    "8)": " good ",
    ":-)": " good ",
    ":)": " good ",
    ";)": " good ",
    "(-:": " good ",
    "(:": " good ",
    "yay!": " good ",
    "yay": " good ",
    "yaay": " good ",
    "yaaay": " good ",
    "yaaaay": " good ",
    "yaaaaay": " good ",
    ":/": " bad ",
    ":&gt;": " sad ",
    ":')": " sad ",
    ":-(": " bad ",
    ":(": " bad ",
    ":s": " bad ",
    ":-s": " bad ",
    "&lt;3": " heart ",
    ":d": " smile ",
    ":p": " smile ",
    ":dd": " smile ",
    "8)": " smile ",
    ":-)": " smile ",
    ":)": " smile ",
    ";)": " smile ",
    "(-:": " smile ",
    "(:": " smile ",
    ":/": " worry ",
    ":&gt;": " angry ",
    ":')": " sad ",
    ":-(": " sad ",
    ":(": " sad ",
    ":s": " sad ",
    ":-s": " sad ",
    r"\br\b": "are",
    r"\bu\b": "you",
    r"\bhaha\b": "ha",
    r"\bhahaha\b": "ha"}



print("....start....cleaning")



#=================stop word=====================


from nltk.stem.wordnet import WordNetLemmatizer 
lem = WordNetLemmatizer()

stop_words = ['the','a','an','and','but','if','or','because','as','what','which','this','that','these','those','then',
              'just','so','than','such','both','through','about','for','is','of','while','during','to']

import string

from nltk.corpus import stopwords

eng_stopwords = set(stopwords.words("english"))



#=================replace the duplicate word=====================
import re

def substitute_repeats_fixed_len(text, nchars, ntimes=3):
    
         Find substrings that consist of `nchars` non-space characters
         and that are repeated at least `ntimes` consecutive times,
         and replace them with a single occurrence.
         Examples: 
         abbcccddddeeeee -> abcde (nchars = 1, ntimes = 2)
         abbcccddddeeeee -> abbcde (nchars = 1, ntimes = 3)
         abababcccababab -> abcccab (nchars = 2, ntimes = 2)
    
    return re.sub(r"(\S{{{}}})(\1{{{},}})".format(nchars, ntimes-1), r"\1", text)

def substitute_repeats(text, ntimes=3):
        # Truncate consecutive repeats of short strings
        for nchars in range(1, 20):
            text = substitute_repeats_fixed_len(text, nchars, ntimes)
        return text



#=================choose one of tokenizer=======================
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

from nltk.tokenize import TweetTokenizer

tokenizer=TweetTokenizer()


#=================final clean function=======================
def clean(comment, remove_stopwords=True, remove_punctuations=False):
    #comment=re.sub("\.\."," .",comment)
    comment=remove_urls(comment.lower())
    #remove \n
    comment=re.sub(r"\t"," ",comment)
    comment=re.sub(r"\r\n"," . ",comment)
    comment=re.sub(r"\r"," . ",comment)
    comment=re.sub(r"\n"," . ",comment)
    comment=re.sub(r"\\n\n"," . ",comment)
    comment=re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","",comment)
    comment=re.sub("\[\[.*\]","",comment)
    comment = re.sub(r"\'ve", " have ", comment)
    
    comment = re.sub(r"\'d", " would ", comment)
    comment = re.sub(r"\'ll", " will ", comment)
    comment = re.sub(r"ca not", "cannot", comment)
    comment = re.sub(r"you ' re", "you are", comment)
    comment = re.sub(r"wtf","what the fuck", comment)
    comment = re.sub(r"i ' m", "I am", comment)
    comment = re.sub(r"I", "one", comment)
    comment = re.sub(r"II", "two", comment)
    comment = re.sub(r"III", "three", comment)
    comment=re.sub(r"mothjer","mother",comment)
    comment=re.sub(r"nazi","nazy",comment)
    comment=re.sub(r"withought","with out",comment)
    comment=substitute_repeats(comment)
    s=comment
    

    
    s = s.replace('&', '')
    s = s.replace('@', '')
    s = s.replace('0', '')
    s = s.replace('1', '')
    s = s.replace('2', '')
    s = s.replace('3', '')
    s = s.replace('4', '')
    s = s.replace('5', '')
    s = s.replace('6', '')
    s = s.replace('7', '')
    s = s.replace('8', '')
    s = s.replace('9', '')
    # s = s.replace('雲水','')

    comment=s
    #comment = re_tok.sub(' ', comment)
    #print(comment)
    words=tokenizer.tokenize(comment)
    words=[no_abbre[word] if word in no_abbre else word for word in words]
    wocomment=substitute_repeats(comment)
rds=[emoji[word] if word in emoji else word for word in words]
    if remove_stopwords:
        words = [w for w in words if not w in stop_words]
    
    sent=" ".join(words)
    # Remove some special characters, or noise charater, but do not remove all!!
    if remove_punctuations:
        sent = re.sub(r'([\'\"\/\-\_\--\_])',' ', sent)
    else:
        sent = re.sub(r'([\'\"\/\-\_\-\_\(\)\{\}])',' ', sent)
    clean_sent= re.sub(r'([\;\|•«\n])',' ', sent)
    clean_sent = re.sub(r"n't", " not ", clean_sent)
    
    FLAG_remove_non_ascii =True
    if FLAG_remove_non_ascii:
        return clean_sent.encode("ascii", errors="ignore").decode().strip()
    else:
        return clean_sent.strip()"""

