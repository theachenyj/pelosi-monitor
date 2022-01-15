import csv, json, zipfile
import requests, PyPDF2, fitz
import pandas as pd

zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/'
ifttt_url = 'https://maker.ifttt.com/trigger/pelosi_monitor/with/key/bVGEDkrCumRST4bL2kYcoC'
csv_path = '/root/pelosi-monitor/last_data.csv'


doc_list = {'date':[], 'doc':[]}
last_data_len = 0

r = requests.get(zip_file_url)
zipfile_name = '2021.zip'

with open(zipfile_name, 'wb') as f:
    f.write(r.content)

with zipfile.ZipFile(zipfile_name) as z:
    z.extractall('.')

with open('2021FD.txt') as txt_file:
    for line in csv.reader(txt_file, delimiter='\t'):
        if line[1] == 'Pelosi':
            doc_list['date'].append(line[7])
            doc_list['doc'].append(line[8])
print(doc_list)
# 如果新的doc_list比上一次的doc_list多，说明发布了新的报告
with open('last_data.csv') as f:
    last_data_len = len(f.readlines())
if len(doc_list['doc']) > last_data_len-1:
    payload = {
        'value1': 'Pelosi 有新的交易！'
    }
    requests.post(ifttt_url, params=payload)
else:
    payload = {
        'value1': '没有披露新的报告。'
    }
    requests.post(ifttt_url, params=payload)


# 更新上一次数据
df = pd.DataFrame(data=doc_list)
df.to_csv('last_data.csv')





#            r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
#
#            with open(f"{doc_id}.pdf", 'wb') as pdf_file:
#                pdf_file.write(r.content)


# doc = fitz.open('20020208.pdf')
#
# page = doc.load_page(page_id=0)
#
# print(page.get_text('json'))

# json_data = page.get_text('json')
#
# json_data = json.loads(json_data)
#
# print(json_data.keys())
#
# for block in json_data['blocks']:
#     if 'lines' in block:
#         print(block)



