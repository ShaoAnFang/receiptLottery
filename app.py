import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort, json

specialPrizeNumber=''
grandPrizeNumber=''
firstPrizeNumbers=[]
addSixPrizeNumbers=[]

app = Flask(__name__)

@app.route('/GGWP', methods=['GET'])
def test():
    return "Hello World!"

def verify(number):
    global specialPrizeNumber
    global grandPrizeNumber
    global firstPrizeNumbers
    global addSixPrizeNumbers
    result = '銘謝惠顧'
    if number == specialPrizeNumber:
        result = '特別獎 1,000萬元'
        #print("特別獎 1,000萬元")
        return result

    if number == grandPrizeNumber:
        result = '特獎 200萬元'
        #print("特獎 200萬元")
        return result

    for fPN in firstPrizeNumbers:
        if number == fPN:
            result = '頭獎 20萬元'
            #print("頭獎 20萬元")

        elif number[1:8] == fPN[1:8]:
            result = '二獎 4萬元'
            #print("二獎 4萬元")
            #print(number[1:8],fPN[1:8])
        elif number[2:8] == fPN[2:8]:
            result = '三獎 1萬元'
            #print("三獎 1萬元")

        elif number[3:8] == fPN[3:8]:
            result = '四獎 4千元'
            #print("四獎 4千元")

        elif number[4:8] == fPN[4:8]:
            result = '五獎 1千元'
            #print("五獎 1千元")
    
        elif number[5:8] == fPN[5:8]:
            result = '六獎 2百元'
            #print("六獎 2百元")
        else:
            for aSPN in addSixPrizeNumbers:
                if number[5:8] == aSPN:
                    result = '增開六獎 2百元'
                    #print("增開六獎 2百元")

    return result

@app.route('/gg/<string:date>/<string:number>', methods=['GET'])
def apii(date,number):
    
    #url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_10701/'
    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_{}/'.format(date)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    
    #print(soup)
    global specialPrizeNumber
    global grandPrizeNumber
    global firstPrizeNumbers
    global addSixPrizeNumbers
    
    specialPrize = soup.find('th', id = "specialPrize").text
    #print(specialPrize)
    specialPrizeNumber = soup.find('td', class_ = "number", headers = "specialPrize").text.strip()
    print(specialPrizeNumber)
    
    grandPrize = soup.find('th', id = "grandPrize").text
    #print(grandPrize)
    grandPrizeNumber = soup.find('td', class_ = "number", headers = "grandPrize").text.strip()
    #print(grandPrizeNumber)

    firstPrize = soup.find('th', id = "firstPrize").text
    #print(firstPrize)
    firstPrizeNumber = soup.find('td', class_ = "number", headers = "firstPrize").text.strip()
    #print(firstPrizeNumber)

    firstPrizeNumbers = firstPrizeNumber.split('、')

    #print("二獎	末7位數與頭獎末7位相同 獎金4萬元")
    #print("三獎	末7位數與頭獎末6位相同 獎金1萬元")
    #print("四獎	末7位數與頭獎末5位相同 獎金4千元")
    #print("五獎	末7位數與頭獎末4位相同 獎金1千元")
    #print("六獎	末7位數與頭獎末3位相同 獎金2百元")

    addSixPrize = soup.find('th', id = "addSixPrize").text
    print(addSixPrize)
    addSixPrizeNumbers = soup.find('td', class_ = "number", headers = "addSixPrize").text.strip()
    addSixPrizeNumbers = addSixPrizeNumbers.split('、')
    print(addSixPrizeNumbers)
    r = verify(number)
    g = dict()
    g['result'] = r
    response=json.dumps(g)
    return response



if __name__ == "__main__":
    app.run()
