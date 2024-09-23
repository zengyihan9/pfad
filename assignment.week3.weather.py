from gettext import install
import requests
from bs4 import BeautifulSoup as bs

url = "http://scstac.oceanguide.org.cn/index.htm"
response = requests.get(url)
if(response.ok):
    print("Data is ready!")
else:
    print(response.status_code)

content =  response.text
soup = bs(content,"html.parser")

tideData = []
tides = soup.find_all("td")

for tide in tides:
    tideValue = tide.string
    if tideValue is not None and tideValue.strip():
        try:
            tideData.append(float(tideValue.strip())) 
        except ValueError:
            continue 

print(f"Total data points: {len(tideData)}")
print(tideData[:100])

import matplotlib.pyplot as plt
import numpy as np

tideData = np.random.uniform(low=0, high=5, size=100)
time_points = np.arange(len(tideData))

plt.figure(figsize=(12, 6))
plt.plot(time_points, tideData, marker='o', linestyle='-', color='b', label='潮汐数据')

plt.title('潮汐数据可视化', fontsize=16)
plt.xlabel('时间点', fontsize=14)
plt.ylabel('潮汐高度', fontsize=14)

plt.grid(True)
plt.legend()

plt.show()
