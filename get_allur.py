import pandas as pd
import feapder
import csv
import os


def write_dict_to_csv(file_path, data_dict, delimiter=',', quotechar='"'):
    """
    将字典数据写入CSV文件。

    :param file_path: CSV文件的路径。
    :param data_dict: 要写入文件的字典数据，其中字典的键将作为列标题。
    :param delimiter: CSV文件的分隔符，默认为逗号。
    :param quotechar: CSV文件的引号字符，默认为双引号。
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 构建完整的文件路径
    full_file_path = os.path.join(current_dir, file_path)

    # 检查是否是首次写入数据，如果是，则将键作为表头写入
    header = list(data_dict.keys())

    # 判断文件是否存在
    file_exists = os.path.isfile(full_file_path)

    # 使用'a'模式打开文件，如果文件存在则追加，否则创建新文件
    with open(full_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        if not file_exists:
            # 文件不存在，创建一个DictWriter并写入表头
            writer = csv.DictWriter(
                csvfile, fieldnames=header, delimiter=delimiter, quotechar=quotechar)
            writer.writeheader()
        else:
            # 文件存在，不需要写入表头
            writer = csv.DictWriter(
                csvfile, fieldnames=header, delimiter=delimiter, quotechar=quotechar)

        # 写入字典数据
        writer.writerow(data_dict)


class AirSpiderDemo(feapder.AirSpider):
    def __init__(self, **kwargs):
        super(AirSpiderDemo, self).__init__(**kwargs)

    def start_requests(self):

        code_list = [{'name': 'Eophona migratoria', 'code': 'yebgro1'}, {'name': 'Turdus mandarinus', 'code': 'chibla1'}, {'name': 'Copsychus saularis', 'code': 'magrob'}, {'name': 'Enicurus leschenaulti', 'code': 'whcfor1'}, {'name': 'Passer montanus', 'code': 'eutspa'}, {'name': 'Emberiza cioides', 'code': 'meabun1'}, {'name': 'Chloris sinica', 'code': 'origre'}, {'name': 'Lonchura punctulata', 'code': 'nutman'}, {'name': 'Phoenicurus fuliginosus', 'code': 'plured1'}, {'name': 'Lonchura striata', 'code': 'whrmun'}, {'name': 'Passer cinnamomeus', 'code': 'russpa2'}, {'name': 'Myophonus caeruleus', 'code': 'blwthr1'}]




        #code_list = [{'name': 'Ixos mcclellandii', 'code': 'moubul2'}, {'name': 'Hemixos castanonotus', 'code': 'chebul1'}, {'name': 'Aegithalos concinnus', 'code': 'blttit2'}, {'name': 'Horornis fortipes', 'code': 'bfbwar1'}, {'name': 'Abroscopus albogularis', 'code': 'rufwar1'}, {'name': 'Aegithalos glaucogularis', 'code': 'lottit5'}]


        #code_list =

        url = "https://media.ebird.org/api/v2/search"  # 首次请求 获取initialCursorMark
        for i in code_list:
            params = {
                "taxonCode": i['code'],
                "mediaType": "photo",
                "birdOnly": "true",
            }
            yield feapder.Request(url, params=params, method="GET", callback=self.post_search, name=i['name'])

    def download_midware(self, request):
        request.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://media.ebird.org/catalog?taxonCode=mouhae1&mediaType=photo",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        request.cookies = {
            "_gcl_au": "1.1.1488880407.1728384520",
            "_gid": "GA1.3.628945833.1728384521",
            "hubspotutk": "b5e4a9fdbb8d08466c5f84a8ed0ade6c",
            "i18n_redirected": "en",
            "ml-search-session": "eyJ1c2VyIjp7ImFub255bW91cyI6dHJ1ZX19",
            "ml-search-session.sig": "SjUzp_aBI4snTlng2qDJ7TZcb2w",
            "_ga": "GA1.2.1922577594.1728384521",
            "_d0371": "b9f60534702d9ec8",
            "__hssrc": "1",
            "__hstc": "60209138.b5e4a9fdbb8d08466c5f84a8ed0ade6c.1728384529940.1728450549814.1728456970435.4",
            "_ga_CYH8S0R99B": "GS1.1.1728461353.5.0.1728461353.60.0.0",
            "_ga_YT7Y2S4MBX": "GS1.1.1728461353.5.0.1728461353.0.0.0",
            "_ga_QR4NVXZ8BM": "GS1.1.1728461353.5.0.1728461353.60.0.0",
            "_ga_4RP6YTYH7F": "GS1.1.1728461353.5.0.1728461353.0.0.0"
        }
        return request

    def post_search(self, request, response):
        for data in response.json:
            assetId = data.get("assetId", None)
            if assetId == None:
                return None
            else:
                # 图片链接
                url = f"https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{assetId}/320"
                item = {}
                item['鸟类'] = request.name
                item['img_url'] = url
                path = "ebird_url.csv"
                write_dict_to_csv(path, data_dict=item)

        # 读取CSV文件
        df = pd.read_csv(path)
        # 计算特定鸟类的数量
        count = df[df['鸟类'] == request.name].shape[0]
        print(f"当前查询鸟类 {request.name} 数量 {int(count)} {int(count)<1000}")

        # 如果数量小于1000，执行某些操作
        if int(count) < 300:
            url = "https://media.ebird.org/api/v2/search"
            params = {
                "taxonCode": request.params['taxonCode'],
                "mediaType": "photo",
                "birdOnly": "true",
                "initialCursorMark": response.json[29]["cursorMark"],
            }
            yield feapder.Request(url, params=params, method="GET", callback=self.post_search, name=request.name)



if __name__ == "__main__":
    AirSpiderDemo(thread_count=1).start()
