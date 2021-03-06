import argparse
import datetime
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from time import sleep

import gspread
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials


parser = argparse.ArgumentParser()
parser.add_argument('--credential-json', type=str, required=True,
                    help='Path to google api credential json file.')
parser.add_argument('--spreadsheet-key', type=str, required=True,
                    help='Google spreadsheet key.')
parser.add_argument('--chromedriver', type=str, required=True,
                    help='Path to chromedriver (Default: ./chromedriver).')
parser.add_argument('--sumgo-id', type=str, required=True,
                    help='Sumgo ID.')
parser.add_argument('--sumgo-pw', type=str, required=True,
                    help='Sumgo password.')
args = parser.parse_args()

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
json_file_name = args.credential_json
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_key = args.spreadsheet_key

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(args.chromedriver, options=op)

url = "https://soomgo.com/login"
driver.get(url)

driver.find_element_by_id('__BVID__63').clear()
driver.find_element_by_id('__BVID__63').send_keys(args.sumgo_id)

driver.find_element_by_id('__BVID__65').clear()
driver.find_element_by_id('__BVID__65').send_keys(args.sumgo_pw)

driver.find_element_by_xpath('//*[@id="app-body"]/div/div/form/div/div[4]/button').click()
try:
    driver.find_element_by_xpath('//*[@id="__BVID__125___BV_modal_footer_"]/button').click()
except:
    print('no ad')

sleep(3)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
sleep(3)

request_list = driver.find_element_by_xpath('//*[@id="app-body"]/div/div[3]/div/ul')
requests = request_list.find_elements_by_tag_name('li')

links = []
for request in requests:
    link = request.find_elements_by_tag_name('a')
    if len(link) != 0:
        links.append(link[0].get_attribute('href'))

data = {}
for idx, link in enumerate(tqdm(links)):
    driver.get(link)
    sleep(5)

    if idx == 0:
        driver.find_element_by_xpath('//*[@id="quote-consulting-tutorial___BV_modal_footer_"]/button').click()
        sleep(1)

    name = driver.find_element_by_xpath('//*[@id="app-body"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div/h4').text
    lesson = driver.find_element_by_xpath('//*[@id="app-body"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/h6[1]').text
    location = driver.find_element_by_xpath('//*[@id="app-body"]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/h6[2]').text

    if lesson not in data:
        data[lesson] = {'??????': [], '??????': []}

    data[lesson]['??????'].append(name)
    data[lesson]['??????'].append(location)

    request_list = driver.find_element_by_xpath('//*[@id="app-body"]/div/div[1]/div[1]/div/div[4]/ul')
    requests = request_list.find_elements_by_tag_name('li')

    real_idx = 0
    for request in requests:
        question = request.find_element_by_xpath('.//p[1]').text
        answer = request.find_element_by_xpath('.//p[2]').text

        if question not in data[lesson]:
            data[lesson][question] = []
        data[lesson][question].append(answer)
        real_idx = len(data[lesson][question])

    for k, v in data[lesson].items():
        if len(v) != real_idx:
            data[lesson][k].append('')
driver.quit()

for k, v in data.items():
    df = pd.DataFrame(v)
    df['????????? ??????'] = datetime.datetime.now()

    try:
        df_org = g2d.download(spreadsheet_key, k, col_names=True, row_names=True, credentials=credentials)
        cols = list(df_org.columns)
        cols.remove('????????? ??????')
        df = pd.concat([df_org, df]).drop_duplicates(subset=cols)
        df = df.reset_index(drop=True)
    except:
        pass

    d2g.upload(df, spreadsheet_key, k, credentials=credentials, row_names=True)

