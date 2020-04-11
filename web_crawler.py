import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from IPython.display import HTML

url = 'http://finance.sina.com.cn/7x24/'
driver = webdriver.Chrome(executable_path="chromedriver.exe")#打开浏览器
driver.get(url)#打开你的访问地址
# driver.maximize_window()#将页面最大化

counter = 0

target_counter = 300

target_keywords = ["特朗普","美国"]

def count_news():
    html = BeautifulSoup(driver.page_source, features="html.parser")
    extracted_news = html.find_all('div', {'class': 'bd_i bd_i_og clearfix'})
    return len(extracted_news)

#把下拉条往下拉..直到获取需要的新闻数目
while counter<target_counter:
    for i in range(5):
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
    counter = count_news()
    print(counter)


html = BeautifulSoup(driver.page_source,features="html.parser")

df = pd.DataFrame(columns=['time','news'])

extracted_news = html.find_all('div', {'class': 'bd_i bd_i_og clearfix'})

valid_news_counter = 0

for each_news in extracted_news:
    title = each_news.find('p', {'class': "bd_i_txt_c"}).getText()
    time_stamp_str = each_news.find('p', {'class': "bd_i_time_c"}).getText()
    for each_keyword in target_keywords:
        if each_keyword in title:
            row_df = pd.DataFrame([time_stamp_str,title])
            df = pd.concat([df,row_df], ignore_index=True)
            valid_news_counter+=1
            print("=====有效信息========")
            print(valid_news_counter)
            print(title)
            print(time_stamp_str)
            break



save_file_name = "sina_news_" + str(time.time()) + ".csv"
df.to_csv(save_file_name,encoding="utf-8-sig")

print("完成，本次提取",len(extracted_news), "条最新新闻，获取有效信息",valid_news_counter, "条")




