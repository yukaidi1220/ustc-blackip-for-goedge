import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 获取网页内容
url = 'https://blackip.ustc.edu.cn/list.php?s=t'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

# 解析网页内容
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('tr')[1:]  # 跳过表头行

# 创建 CSV 文件
with open('blacklist_ips.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    for row in rows:
        columns = row.find_all('td')
        start_time = columns[0].text.strip()
        end_time = columns[1].text.strip()
        ip = columns[2].text.strip()
        remark = columns[3].text.strip()
        
        try:
            # 只处理 IPv4 地址
            if '.' in ip:
                # 计算过期时间戳
                end_time_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                end_time_ts = int(end_time_dt.timestamp())
                
                writer.writerow([ip, end_time_ts, 'ipv4', 'critical', remark])
        except ValueError:
            # 忽略无法解析的日期
            continue

print("CSV 文件已生成：blacklist_ips.csv")
