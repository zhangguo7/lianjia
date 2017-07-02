# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def get_districts(root_url,headers):
    """获取区县信息

    :param root_url:根url: https://cd.lianjia.com/chengjiao/
    :param headers: 请求头
    :return: 区县信息构成的字典
    """
    res = requests.get(url=root_url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    div = soup.find('div',{'data-role':'ershoufang'})
    districts = div.find_all('a')
    districts_dict = {}

    for i,district in enumerate(districts):
        pa = re.compile('href="(.*?)" title.*?">(.*?)</a>')
        semi_url, name = pa.findall(str(district))[0]
        url = 'https://cd.lianjia.com'+semi_url
        districts_dict['%s'%name] = url

    return districts_dict

def get_block(districts):
    """通过区县信息返回block信息

    :param districts: 区县信息构成的字典
    :return: 生成器，用于迭代每个block的成交
    """
    for district in districts.items():
        district_name,district_url = district
        res = requests.get(district_url,headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        div = soup.find('div', {'data-role': 'ershoufang'})
        blocks = div.find_all('a')
        for i, block in enumerate(blocks):
            try:
                pa = re.compile('href="(.*?)">(.*?)</a>')
                semi_url, name = pa.findall(str(block))[0]
                if name not in districts:
                    block_sample = {
                        'district_name': district_name,
                        'district_url': district_url,
                        'block_name': name,
                        'block_url': 'https://cd.lianjia.com'+semi_url
                    }
                    yield block_sample
            except Exception as e:
                raise Exception('district_name=%s,district_url=%s,'
                                'block can not be extract'%district)


def get_maxpage(block_sample,phjs_driver):
    driver.get(block_sample['block_url'])
    text = driver.page_source



if __name__ == '__main__':
    root_url = 'https://cd.lianjia.com/chengjiao/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'
    }
    districts = get_districts(root_url,headers)
    block_ge = get_block(districts)
    driver = webdriver.PhantomJS()
    block_sample = next(block_ge)
    driver.get(block_sample['block_url'])
    print(driver.page_source())