import os
import csv
import json
import datetime
import requests
from bs4 import BeautifulSoup


yahoo_booth_csv = './booth.csv'
booth_url_endpoint = 'https://tw.bid.yahoo.com/booth/'
if os.path.isfile(yahoo_booth_csv) is False:
    print('The booth.csv file is not found.')
    exit(1)


csv_handler = open(yahoo_booth_csv, 'r')
contents = csv_handler.readlines()
if contents[-1] == '':
    contents = contents[0:-1]

for content in contents:
    content = content.replace('\n', '')
    content = content.replace('\r', '')
    booth_lists = csv.reader([content])
    break


booth_links = ''
year = datetime.datetime.now().strftime('%Y')
first_column = ''
second_column = ''


for booth_id in list(booth_lists)[0]:
    booth_url = booth_url_endpoint + booth_id


    response = requests.get(booth_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    bid_data = json.loads(soup.select_one("#isoredux-data")['data-state'])
    hit_bid_datasets = bid_data['booth']['listings']['hits']

    booth_name = bid_data['booth']['name']
    booth_links += '<li><a href="%s">%s</a></li>' % (booth_url, booth_name)

    index = 0
    for hit_bid_data in hit_bid_datasets:
        title = hit_bid_data['title']
        url = hit_bid_data['url']
        in_stock = hit_bid_data['inStock']
        img_src = hit_bid_data['imgs'][0]['src']

        in_stock_message = '缺貨中'
        if in_stock is True:
            in_stock_message = '有現貨'

        column_record_format = '''
<tr>
    <td style="padding-top: 20px; padding-left: 10px;">
        <a href="{0}"><img src="{1}" alt="" style="width: 100%; max-width: 600px; height: auto; margin: auto; display: block;"></a>
        <div class="text-project" style="text-align: center;">
       	    <h3><a href="{2}">{3}</a></h3>
     	    <span>{4}</span>
        </div>
    </td>
</tr>
'''

        if index % 2 == 0:
            first_column += column_record_format.format(url, img_src, url, title[0:6] + '...', in_stock_message)
        else:
            second_column += column_record_format.format(url, img_src, url, title    [0:6] + '...', in_stock_message)

        index += 1


print('Generating the Newsletter...')

handler = open('./email_template/index.html.template', 'r', encoding='utf-8')
email_template = handler.read()
handler.close()

email_template = email_template.replace('{first_column}', first_column)
email_template = email_template.replace('{second_column}', second_column)
email_template = email_template.replace('{booth_links}', booth_links)
email_template = email_template.replace('{year}', year)

handler = open('./index.html', 'w', encoding='utf-8')
handler.write(email_template)
handler.close()

print('Generating the Newsletter is done!')
