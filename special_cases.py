from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
import possible_errors as pe
class is_pinterest():
    def __init__(self):
        # 以后用到再说，现在pinterest是用动态爬的，没有这个问题
        pass

class is_webarchive():
    def __init__(self,url):
        self.url=url
    def return_url(self):
        # 回去看一下webarchive上的图片链接到底是怎么写的，这个样子是没办法直接扔到下载代码里面去的
        return ('http' + (self.url).split('http')[-1])

class is_tistory():
    def __init__(self,url):
        self.url=url

    def return_url(self):
        url=self.url
        if 'daumcdn' in url and 'fname' in url:
            url1 = url.split('=')[-1]
            url2 = unquote(url1)
            url2 = url2.replace('image', 'original')
            self.url = url2
        else:
            if 'image' in url and 'cfile' in url:
                url3 = url.replace('image', 'original')
                self.url = url3
            else:
                self.url = url
        return self.url

class is_kpoping:
    def __init__(self,url):
        self.url=url

    def return_url(self):
        url=self.url

        return 'https://www.kpoping.com'+url

class url_cleaning():
    def __init__(self,url):
        self.url=url
    def return_keyword_list(self):
        if 'tistory.com' in self.url:
            return ['img_bnr.png','crop','Banner01.png','bottom.png','top.png',
                    'icon','copyright','menu']
        else:
            return []

class blog_naver():
    def __init__(self,url):
        if url is None:
            raise pe.url_error
        self.url=url


    def clean_url(self,url=None):
        if url is None:
            url=self.url

        if type(url) is not str:
            raise TypeError
        if 'logNo' in url:
            logNo = url.split('logNo=')[-1].split('&')[0]
            user = url.split('blogId=')[-1].split('&')[0]
            return 'https://blog.naver.com/' + user + '/' + logNo
        else:
            return url

    def get_blog_naver_iframe(self,url=None):
        if url is None:
            url=self.url
        with requests.get(url) as x:
            x.encoding = x.apparent_encoding
            soup = BeautifulSoup(x.text, 'lxml')
            actual_url = soup.find('iframe', attrs={'id': 'mainFrame'}).get('src')
        return 'https://blog.naver.com' + actual_url

    def get_true_link(self,url=None):
        if url is None:
            url=self.url
        clear_url = self.clean_url(url)
        final_url = self.get_blog_naver_iframe(clear_url)
        return final_url

    def clean_pic_url(self,img_url):
        return img_url.replace('postfiles','blogfiles').split('?type')[0]

if __name__ == '__main__':
    print(blog_naver('https://blog.naver.com/mondlicht119/220777984745').get_true_link())