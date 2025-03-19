import os
import re
import feapder


import csv

def read_csv_to_dict(csv_file_path):
    """
    读取CSV文件，并将第0列作为键，第1列作为值，存储到一个OrderedDict中。

    :param csv_file_path: CSV文件的路径。
    :return: 包含CSV文件数据的OrderedDict。
    """
    data_list = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 如果CSV文件有标题行，跳过标题行
        for row in reader:
            if row:  # 确保行不是空的
                try: #
                    key = row[0]
                    value = row[1]
                except IndexError:
                    continue
                data_list.append({"鸟类":key,"链接":value})
    return data_list

# 使用示例
csv_file_path = 'ebird_url.csv'  # 替换为你的CSV文件路径
data_dict = read_csv_to_dict(csv_file_path)


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        for data in data_dict:
            url = data['链接']
            name = data['鸟类']
            yield feapder.Request(url, method="GET",name=name)

    def download_midware(self, request):
        request.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        return request

    def parse(self, request, response):
        # 获取当前运行目录
        current_dir = os.getcwd()

        # 创建文件夹路径
        folder_path = os.path.join(current_dir, request.name)

        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        pattern = r'/api/v2/asset/(\d+)/'
        match = re.search(pattern, request.url).group(1)

        # 创建图片完整路径
        image_path = os.path.join(folder_path, f"{match}.png")
        
        with open(image_path, 'wb') as f:
            f.write(response.content)

if __name__ == "__main__":
    AirSpiderDemo(thread_count=16).start()
        