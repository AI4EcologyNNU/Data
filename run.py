import feapder
import re
import os


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        name = [

            "Numenius phaeopus",
            "Nycticorax nycticorax",
            "Otus lettia",
            "Otus semitorques",
            "Parus minor",
            # "Passer cinnamomeus",
            # "Passer montanus",
            # "Pericrocotus solaris",
            # "Pericrocotus speciosus",
            # "Phasianus colchicus",
            # "Phoenicurus fuliginosus",
            # "Phylloscopus plumbeitarsus"


        ]
        for i in name:
            url = "https://xeno-canto.org/api/internal/completion/species"
            params = {
                "query": i
            }
            yield feapder.Request(url, params=params, method="GET")

    def download_midware(self, request):
        request.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "priority": "u=1, i",
            "referer": "https://xeno-canto.org/explore?query=Phylloscopus-plumbeitarsus",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        request.cookies = {
            "__utma": "47666734.1288040778.1733116882.1733116882.1733116882.1",
            "__utmz": "47666734.1733116882.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "PHPSESSID": "sh2fpq6uaokbl5ecdsfqda01nr",
            "__utmc": "47666734",
            "__utmt": "1",
            "__utmb": "47666734.17.10.1733116882"
        }
        return request

    def parse(self, request, response):
        print(response.json)
        try:
            conut = int(response.json["data"][0]["recordings"])
        except:
            print(f"暂未搜索到{request.params['query']}")
            return
        url = "https://xeno-canto.org/explore"
        name = request.params['query']
        for pg in range(1,(conut//30)+1):
            params = {
            "query": name,
            "pg":pg
            }
            yield feapder.Request(url, params=params, method="GET",callback=self.parse_two)
            
    def parse_two(self, request, response):
        # 假设这是包含多个链接的列表
        links_list = response.xpath('//a/@href').extract()
        name = request.params['query']
        # 正则表达式模式，匹配以 https://xeno-canto.org/ 开头，后面跟着数字，以 /download 结尾的URL
        pattern = re.compile(r'https://xeno-canto.org/\d+/download')

        # 用来存储匹配的链接
        matching_links = []

        # 遍历列表，检查每个链接是否符合正则表达式
        for link in links_list:
            if pattern.match(link):
                matching_links.append(link)

        # 打印匹配的链接
        for link in matching_links:
            yield feapder.Request(link,method="GET",callback=self.download,name=name)
            
    def download(self, request, response):
        save_dir = f'./{request.name}'  # 在当前运行目录下保存
        pattern = r'https://xeno-canto.org/(\d+)/download'

        # 使用正则表达式搜索数字
        match = re.search(pattern, request.url)

        number = match.group(1)
        save_path = os.path.join(save_dir, f'{number}.mp3')  # 文件全路径

        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
            # 以二进制写入模式打开文件
        with open(save_path, 'wb') as file:
                # 写入内容
            file.write(response.content)
            print(f'文件已保存到：{save_path}')

if __name__ == "__main__":
    AirSpiderDemo(thread_count=16).start()
        