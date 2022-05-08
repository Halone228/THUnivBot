import aiohttp
from bs4 import BeautifulSoup
from keyboards import CallBackDatas
import asyncio


def read_file(name) -> BeautifulSoup:
    with open(fr'html\{name}.html', 'r', encoding='utf-8') as f:
        raw_html = f.read()
    soup = BeautifulSoup(raw_html, 'lxml')
    return soup


class Parser:
    def __init__(self,loop):
        # print("Parser was started")
        # loop.run_until_complete(self.get_htmls())
        print("Parser inited")

#Abiturient`s Parsers
    @staticmethod
    async def commission_parsing() -> str:
        soup = read_file(CallBackDatas.commission.name)
        address = soup.select_one('div.content-area:nth-child(1) > p:nth-child(2) > strong:nth-child(1)').text.strip()
        table = soup.select_one('#wp-table-reloaded-id-50-no-1 > tbody:nth-child(2)')
        rasp = []
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            day = tds[0].text.strip()
            time = tds[1].text.replace('\n',', ')
            rasp.append(f'{day} --- {time}')
        rasp = "\n".join(rasp)
        return f'Адрес: {address}\n{rasp}'

    @staticmethod
    async def perech_dok_parser() -> str:
        soup = read_file(CallBackDatas.perech_dok.name)
        ol = soup.select_one('.wprt-container > ol:nth-child(5)')
        end_str = ''

        for num,li in enumerate(ol.find_all('li'),start=1):
            a = li.find_all('a')
            a_html_raw = ' '.join([str(aa.extract()) for aa in a])
            end_str += f'{num}. {li.text.strip()} {a_html_raw}\n'
        return end_str

    @staticmethod
    async def zaselenie_parser() -> str:
        soup = read_file(CallBackDatas.zaselenie.name)
        ul = soup.select_one('.wprt-container > ul:nth-child(12)')
        end_str = 'Перечень документов необходимых для заселения:\n'
        for num,li in enumerate(ul.find_all('li'),start=1):
            end_str += f'{num}. {li.text.strip()}\n'
        return end_str

    @staticmethod
    async def specialnosti_parser() -> dict:
        soup = read_file(CallBackDatas.specialnosti.name)
        ul = soup.select_one('#menu-item-8703 > ul:nth-child(2)')
        buttons = [{'text': a.text.strip(), 'url': a.get('href')} for a in ul.find_all('a')]
        return {'args':buttons,'kwargs':{}}

    @staticmethod
    async def prof_teach_text() -> str:
        soup = read_file(CallBackDatas.prof_teach.name)
        text = ''
        text += '<strong>'+str(soup.select_one('.wprt-container > p:nth-child(3)').text.strip())+'</strong>\n'
        text += str(soup.select_one('.wprt-container > p:nth-child(4)').text.strip())
        text += str(soup.select_one('.wprt-container > p:nth-child(5)').text.strip())
        return text

    @staticmethod
    async def prof_teach_keyboard() -> dict:
        soup = read_file(CallBackDatas.prof_teach.name)
        a_s = soup.select_one('.wprt-container > p:nth-child(6)').find_all('a')
        properties = {'args':[{'text':a.text.strip(),'url':a.get('href')}for a in a_s],
                      'kwargs': {}}
        return properties

    #################################################################################################################
    #Another_parser
    ##########################
    @staticmethod
    async def pamyatka_keyboard() -> dict:
        domain = 'https://rbmed03.ru'
        soup = read_file(CallBackDatas.pamyatka.name)
        res_set = soup.select('.elementor-button-link')
        args = []
        print(len(res_set))
        for button in res_set:
            args.append({'text':button.text.strip().capitalize(),
                         'url':domain+button.get('href')})
        return {'args':args,'kwargs':{}}

    @staticmethod
    async def oplata_parser() -> str:
        soup = read_file(CallBackDatas.oplata.name)
        return soup.select_one('.wprt-container > p:nth-child(4)').text.strip()

    @staticmethod
    async def zakaz_spravki() -> dict:
        soup = read_file(CallBackDatas.zakaz_spravki.name)
        div = soup.select_one('.wprt-container')
        args = []
        for a in div.find_all('a'):
            args.append({'text':a.text.strip(),'url':a.get('href')})
        return {'args':args,'kwargs':{}}

    @staticmethod
    async def save_to_html(url,name='index'):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                raw_html = await response.text()
                with open(fr'html\{name}.html','w',encoding='utf-8') as f:
                    f.write(raw_html)

    @classmethod
    async def get_htmls(cls):
        tasks = []
        for en in CallBackDatas:
            if isinstance(en.value, dict) and (en.value.get('text',False)
                                               or
                                               en.value.get('keyboard',{}).get('func',False)):
                tasks.append(cls.save_to_html(en.value['url'],en.name))
        await asyncio.gather(*tasks)

    @classmethod
    def get_method_by_name(cls,name:str):
        return cls.__dict__.get(name)