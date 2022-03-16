#!python3.9

import requests as rqs
from bs4 import BeautifulSoup as bsp

class GetProblem:
    def __init__(self):
        self.test_data = {'sample_input': '', 'sample_output': ''}

        self.url = 'https://dandanjudge.fdhs.tyc.edu.tw/'
        self.pid = 'a001'

    def process_textpre(self, content, pkeys: list, name: str): # 範例輸入、範例輸出
        pkeys_id = 0
        for i in content:
            ok = False
            text = ''
            for j in i.find_all(name=name):
                text_list = j.text.strip().split('\n')
                for t in text_list:
                    text += t.strip() + '\n'
                ok = True

            if ok:
                self.test_data[pkeys[pkeys_id]] += text
                pkeys_id += 1


    def get_problem(self, _pid):
        self.url, self.pid = 'https://dandanjudge.fdhs.tyc.edu.tw', _pid
        response = None

        try:
            response = rqs.get(f'{self.url}/ShowProblem?problemid={self.pid}')
        except Exception:
            response = rqs.get('https://dandanjudge.fdhs.tyc.edu.tw/ShowProblem?problemid=a001')
        html = bsp(response.text, 'html.parser')
        content = html.find_all(name='div', attrs={'class', 'problembox'})

        self.process_textpre(content, ['sample_input', 'sample_output'], 'pre')

    def get_test_data(self):
        return {
            'input': self.test_data['sample_input'],
            'output': self.test_data['sample_output']
        }

if __name__ == '__main__':
    test = GetProblem()
    test.get_problem('a752')
    test.save_problem('test', './problem')
