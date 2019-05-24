import scrapy, pandas
from scrapy_splash import SplashRequest
import pymysql
from sqlalchemy import create_engine

class QuotesSpider(scrapy.Spider):

    name = "kenh14"
    start_urls = [
        'http://kenh14.vn/'
    ]


    def parse(self, response):
        print("#################### Get links ##################")

        links = []
        BigNewLink       = response.xpath("//h2[@class='klwfnl-title']/a/@href").extract()
        SecondBigNewLink = response.xpath("//h2[@class='klwfnr-title']/a/@href").extract()
        ThirdBigNewLink  = response.xpath("//h2[@class='klwfnswn-title']/a/@href").extract()
        NewNews = response.xpath("//p[@class='inszone1title']/a/@href").extract()
        NewLinks = response.xpath("//h3[@class='knswli-title']/a/@href").extract()

        links = BigNewLink + SecondBigNewLink + ThirdBigNewLink + NewNews + NewLinks

        for link in links:
            yield scrapy.Request("http://kenh14.vn/" + link, callback=self.parse_single_new)

    def parse_single_new(self, response):
        print("#################### Parse single new ##################")
        n_gram = 2
        threshold = 0.5

        con = pymysql.connect('localhost', 'root', '', 'IR')

        with con: 
            cur = con.cursor()
            cur.execute("SELECT short_content FROM news1")
            rows = cur.fetchall()
        x = []
        for item in rows:
            x.extend(item)

        URL = response.request.url
        id = str(URL).rsplit('-', 1)[-1]
        id = id.split('.')[0]
        Title = response.xpath("//h1[@class='kbwc-title']/text()").extract()[0]
        
        Time = response.xpath("//span[@class='kbwcm-time']/@title").extract()[0]
        
        ShortContent = response.xpath("//h2[@class='knc-sapo']/text()").extract()[0][2:-2]

        FullContentArray = response.xpath("//div[@class='knc-content']//p/text()").extract()
        FullContent = get_text_in_fullcontent(FullContentArray)

        compare = jaccard_one_with_all(ShortContent, x, n_gram, threshold)
        if not compare:
            print("OK")
            result = [id, URL, Title, Time, ShortContent, FullContent]
            dataframeResult = pandas.DataFrame([result])
            dataframeResult.columns = ['id', 'url', 'title', 'time', 'short_content', 'full_content']
            # dataframeResult.to_csv("news-data.csv", index=False, mode='a', header=False)
            
            engine = create_engine("mysql+pymysql://root:@localhost/IR")
            with engine.connect() as conn, conn.begin():
                dataframeResult.to_sql(name='news1', con=engine, if_exists = 'append', index=False)
        else:
            print("Trung Lap")

def get_text_in_fullcontent(FullContentArray):
    result = ""
    
    for i in range(len(FullContentArray)):
        result += FullContentArray[i]

    return result

############ Jaccard
def separate_word(sentence1):
    List = []

    flag = 0
    for i in range(len(sentence1)):
        if sentence1[i] == ' ':
            List.append(sentence1[flag:i])
            flag = i+1
        if i == len(sentence1)-1:
            List.append(sentence1[flag:i+1])
    return List

def create_shingles(List, n_gram):
    shingles_list = []

    for i in range(len(List) - n_gram):
        shingle_element = List[i:i+n_gram]
        if shingle_element not in shingles_list :
            shingles_list.append(shingle_element)

    return shingles_list + [List[-2:]]

def jaccard_similarity(sentence1, sentence2, n_gram):
    num = 0
    total = 0

    list1 = separate_word(sentence1)
    list2 = separate_word(sentence2)

    shingles_list1 = create_shingles(list1, n_gram)
    shingles_list2 = create_shingles(list2, n_gram)
    
    total += len(shingles_list1)

    for i in range(len(shingles_list2)):
        flag = True
        for j in range(len(shingles_list1)):
            if shingles_list2[i] == shingles_list1[j]:
                num += 1
                flag = False

        if flag == True:
            total += 1
    
    return num/total

# check one with others all, return True => is similar
def jaccard_one_with_all(sentence, All, n_gram, threshold):
    max_jaccard = 0

    for i in range(len(All)):
        jaccard_number = jaccard_similarity(sentence, All[i], n_gram)
        if jaccard_number > max_jaccard:
            max_jaccard = jaccard_number

    return max_jaccard > threshold