import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import nltk
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import multiprocessing
import pandas as pd
import os
import concurrent.futures
import urllib.request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
nltk.download('punkt')
nltk.download('stopwords')


def removePuncStr(s):
    for c in string.punctuation:
        s = s.replace(c," ")
    return s

# def removePunc(text_array):
#     return [removePuncStr(h) for h in text_array]

def removeNumbersStr(s):
    for c in range(10):
        n = str(c)
        s = s.replace(n," ")
    return s

# def removeNumbers(text_array):
#     return [removeNumbersStr(h) for h in text_array]


def stopText(text_array):
    stop_words = set(stopwords.words('english'))
    stopped_text = []
    words = word_tokenize(text_array)
    h2 = ''
    for w in words:
        if w.lower() not in stop_words:
            h2 = h2 + ' ' + w
    return h2

def stemText(text_array):
    ps = PorterStemmer()
    words = word_tokenize(text_array)
    h2 = ''
    for w in words:
        h2 = h2 + ' ' + PorterStemmer().stem(w)
    return h2

analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score

def load_url(url, timeout):
    f = requests.get(url)
    text = f.text
    f.close()
    only_p_tags = SoupStrainer('p')
    soup = BeautifulSoup(text, 'html.parser', parse_only=only_p_tags)
    text_array = soup.get_text()
    if url.startswith('https://www.cnn'):
        only_div_tags = SoupStrainer('div', class_="zn-body__paragraph")
        soup = BeautifulSoup(text, 'html.parser', parse_only=only_div_tags)
        text_array += soup.get_text()
    clean_data = stopText(stemText(removeNumbersStr(removePuncStr(text_array))))
    return(sentiment_analyzer_scores(clean_data))
def SentimentWorkers(data):
    URLS = data['Url'].to_list()
    result = pd.DataFrame()
# We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            each_url = {executor.submit(load_url, url, 60): url for url in URLS}
            for each_url_result in concurrent.futures.as_completed(each_url):
                result = result.append(each_url_result.result(), ignore_index=True)
    return result
def SentimentBruteForce(data):
    result1 = pd.DataFrame()
    for i in range(len(data)):
        url = ''
        print(f' Predicting Sentiment for {i} of {len(data)}\r', end="")
        url = data.iloc[i]['Url']
        f = requests.get(data.iloc[i]['Url'])
        text = f.text
        f.close()
        only_p_tags = SoupStrainer('p')
        soup = BeautifulSoup(text, 'html.parser', parse_only=only_p_tags)
        text_array = soup.get_text()
        if url.startswith('https://www.cnn'):
            only_div_tags = SoupStrainer('div', class_="zn-body__paragraph")
            soup = BeautifulSoup(text, 'html.parser', parse_only=only_div_tags)
            text_array += soup.get_text()
        clean_data = stopText(stemText(removeNumbersStr(removePuncStr(text_array))))
        result1 = result1.append(sentiment_analyzer_scores(clean_data), ignore_index=True)
    df_final = pd.merge(data, result1, left_index=True, right_index=True)
    return df_final
## Nobias Political Leaning
def ploticalLean(url, timeout):
    dic_r = []
    r = {}
    r_exp = {}
    r_exp = {0: "Article Not Found",
             1: "Article Not Found",
             2: "Article Not Found"}
    for i in range(0,5):
        nobias_url = 'https://demo.nobias.com/?url='+url
        with webdriver.Firefox() as driver:
            try:
                wait = WebDriverWait(driver, 15) #adjust this time depending on your internet speed - may need to raise this if internet is slow
                driver.get(nobias_url)
                results = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.mainText")))
                temp = 0
                for i in results:
                    r[temp] = i.get_attribute("textContent")
                    temp = temp + 1
                    dic_r += [r]
            except:
                 dic_r += [r_exp]
    df_result = pd.DataFrame(dic_r)
    df_result = df_result.rename(columns={0: "Political_Leaning",
                                          1: "Credibility",
                                          2: "Para_len"}, errors="raise")
    return df_result
def PoliticalWorkers(data):
    URLS = data['Url'].to_list()
    result = pd.DataFrame()
# We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            each_url = {executor.submit(ploticalLean, url, 60): url for url in URLS}
            for each_url_result in concurrent.futures.as_completed(each_url):
                result = result.append(each_url_result.result(), ignore_index=True)
    return result
def main():
    if os.name == 'nt':
        os.environ["PATH"] += os.pathsep + os.pathsep.join(["C:\\geckodriver"])
    num_cores = multiprocessing.cpu_count()
    data_csv = pd.read_csv('Master_List_Final.csv')
    # result_sent = SentimentBruteForce(data_csv)
    prompt = input("Do You want to Perform Political Analysis(Resource Heavy, takes few hour to complete) Please?[y/n or Y/N]:")
    result_worker = SentimentWorkers(data_csv)
    result_sent = pd.DataFrame()
    result_sent = pd.merge(data_csv, result_worker, left_index=True, right_index=True)
    result_sent.to_csv('sentiment_score_final.csv')
    if prompt == 'y' or prompt == 'Y':
        df_politc = PoliticalWorkers(data_csv)
        result_politic = pd.DataFrame()
        result_politic = pd.merge(data_csv, df_politc, left_index=True, right_index=True)
        result_politic.to_csv('Nobias_score.csv')
if __name__ == '__main__':
    main()



