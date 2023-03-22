from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests
import os

def url_crawl(result): #36337 36745
    for id in range(36334, 36746):
        #url = 'https://www.fss.or.kr/fss/bbs/B0000206/view.do?nttId=%d&menuNo=200690' %id
        url = 'https://www.fss.or.kr/fss/bbs/B0000207/view.do?nttId=%d&menuNo=200691' %id
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        dbdata = soup.find("div", class_="dbdata")
        video = dbdata.find("video")
        if video is not None:
            link = video["src"]
            result.append(video["src"])
            print("link %d crawled"%id)
    return

def file_down(links):
    i = int(186)
    for link in links:
        i+=1
        response = requests.get(link)
        if response.status_code == 200:
            filename = "voice_file%d.mp3" % i
            directory = "D:\project\webcrawling\mp3file"
            file_path = os.path.join(directory, filename)

            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded {filename} to {directory}")
        else:
            print(f"Failed to download {link} (status code: {response.status_code})")

def main():
    result = []
    print('crawling >>>>>>>>>>>>>')
    url_crawl(result)
    links=[]
    prefix = "https://www.fss.or.kr"
    for link in result:
         mlink = prefix +link
         links.append(mlink)
    #print(links)
    file_down(links)
    del result[:] #다시 시작할때는 이전 작업에서 저장한 내용 삭제

if __name__ == '__main__':
    main()
