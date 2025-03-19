import feapder
import atexit
code_list = []



def print_code_list():
    print("鸟类code列表:")
    print(code_list)

class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        url = "https://api.ebird.org/v2/ref/taxon/find/"
        bird_list = [

                    # 11.27新增


            # "Cyanopica cyanus",
            # "Urocissa erythroryncha",
            # "Dendrocitta formosae",
            # "Pica serica",
            # "Corus torquatus",
            # "Corvus macrorhynchos",
            # "Parus minor",
            # "Alauda arvensis",
            # "Cisticola juncidis",
            # "Prinia inornata",
            # "Spizixos semitorques",
            # "Pycnonotus xanthorrhous",
            # "Pycnonotus sinensis",
            # "Ixos mcclellandii",
            # "Hemixos castanonotus",
            # "Abroscopus albogularis",
            # "Horornis fortipes",
            # "Aegithalos glaucogularis",
            # "Aegithalos concinnus"
            # "Sinosuthora webbiana",
            # "Calamornis heudei",
            # "Zosterops simplex",
            # "Pomatorhinus ruficollis",
            # "Garrulax canorus",
            # "Garrulax monileger",
            # "Pterorhinus perspicillatus",
            # "Pterorhinus pectoralis",
            # "Leiothrix lutea",
            # "Acridotheres cristatellus",
            # "Spodiopsar sericeus",
            # "Spodiopsar cineraceus",
            # "Gracupica nigricollis",
            "Turdus mandarinus",
            "Copsychus saularis",
            "Enicurus leschenaulti",
            "Myophonus caeruleus",
            "Phoenicurus fuliginosus",
            "Lonchura striata",
            "Lonchura punctulata",
            "Passer cinnamomeus",
            "Passer montanus",
            "Eophona migratoria",
            "Emberiza cioides",
            "Chloris sinica"

        ]
        for i in bird_list:
            params = {
                "key": "cnh95enq2brj",
                "locale": "zh-CN",
                "q": i
            }
            yield feapder.Request(url, params=params, method="GET")

    def download_midware(self, request):
        request.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "origin": "https://media.ebird.org",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://media.ebird.org/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        return request

    def parse(self, request, response):
        if response.json != []:
            code = response.json[0]['code']
            code_list.append({"name":request.params['q'],"code":code})
        else:
            print(f'无法找到鸟类{request.params["q"]}')

if __name__ == "__main__":
    atexit.register(print_code_list)
    AirSpiderDemo(thread_count=24).start()
