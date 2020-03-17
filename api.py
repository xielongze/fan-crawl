import sys
import os
import requests
import traceback
import re
from bs4 import BeautifulSoup
import urllib3
from fake_useragent import UserAgent
import possible_errors as pe
import special_cases as sc
import imghdr

class download():
    def __init__(self):
        self.header = {'User-agent': UserAgent().random}
        # self.header = {'User-agent': UserAgent(verify_ssl=False, use_cache_server=False).random}
        # 用于伪装反爬的header

    def setting(self,
                url=None,save_dir='./save/',nodownload_list=[],
                gif=True,
                to_make_son_folder=False,
                verbose=True,resume=True,
                delete=False,is_naver=False,
                min_size=55
                 ):

        if url is None:
            return None
        # 这是一个例外设计，如果不需要用到main函数，而只要用到request_image函数，
        # 那么就没有必要在这里做太多设置了，直接退出这个类就可以

        if 'tistory.com' in url or 'hvstudio.net' in url:
            if '/m/' in url:
                url=url.replace('/m/','/')
            if '?' in url:
                url=url.split('?')[0]
        if url.endswith('/'):
            url=url.strip('/')
        # 下载的链接，对tistory网页做一个清洗，同时去除掉最后那个斜杠，避免在生成文件夹的时候造成误导

        if is_naver:
            self.naver=sc.blog_naver(url)
            self.url=self.naver.clean_url(url)
        else:
            self.url=url

        self.to_make_son_folder = to_make_son_folder
        # 控制是否按照斜线生成文件夹
        # if True，那么就会在save_dir下面再生成子文件夹
        # 如果不需要，那么就直接在指定的save_dir里面保存就可以了

        self.save_dir = save_dir
        # 是否要按照网站生成文件夹，
        # 如果to_make_son_folder==True，那么就在save_dir下面再按照网页斜线生成文件夹
        # 否则直接保存在save_dir下面

        nodownload_list_cleaned=sc.url_cleaning(self.url).return_keyword_list()
        for i in nodownload_list_cleaned:
            nodownload_list.append(i)
        self.nodownload_list=nodownload_list

        self.gif=gif
        # 是否下载后缀为gif的图片

        self.verbose=verbose
        self.resume=resume
        # 这个参数是新增的，含义是是否支持断点传续
        # if resume,在下载图片时不考虑重命名，如果有名称重复的图片，就直接进行覆盖下载
        # 这种情况适用于tistory等网站
        # if not resume，在下载图片时会进行重命名，例如arin1,arin2，适用于tumblr等网站
        # 默认resume==True，即不会重命名图片，而是进行断点传续

        self.delete=delete
        self.is_naver=is_naver
        self.min_size=min_size
        if verbose:
            print('Start downloading from %s '%url)

    def request_page(self,url=None):
        # 访问含有大量图片的页面，并返回所有图片的链接
        # 这个是比较通用的方法，但是并不是万能的，例如pinterest,tumblr等很多网站不能使用这个函数
        # 也是因为这个方法不万能，所以才会要重写这个类
        if url is None:
            url=self.url
            # 做一个默认的赋值
        with requests.get(url,headers=self.header) as x:
            x.encoding=x.apparent_encoding

            soup=BeautifulSoup(x.text,'lxml')
            imgs=soup.find_all('img')

            if imgs is None or imgs==[]:
                raise pe.pic_no_found_error
            # 如果没有找到图片

            print('Found %d pictures' %(len(imgs)))
            for img in imgs:
                src=img.get('src')
                yield src

    def download_single_img(
            self,
            url=None,
            save_dir=None,
            name=None,
            resume=None,
            verbose=None,
            delete=None,
            min_size=None
    ):
        if url is None:
            url=self.url
        try:
            if self.is_naver==True:
                url=self.naver.clean_pic_url(url)
        except AttributeError:
            pass

        if name is None:
            file_name=re.sub('[\\\%$#@^:*?"<>|!]','',url.split('/')[-1])
            # 如果没有传入一个名字，那么就直接用url最后一个斜杠后面的字符作为文件名
            # 注意，这里传进来的名称是没有后缀的，后缀会在后面自动生成
        else:
            file_name=name
            # 名称仍然是可以指定的

        if save_dir is None:
            save_dir=self.save_dir

        if delete is None:
            try:
                delete=self.delete
            except AttributeError:
                delete=False
        if verbose is None:
            verbose=self.verbose
        if file_name.endswith('.jpg') or file_name.endswith('png') or file_name.endswith('gif') or file_name.endswith('jpeg'):
            # 没有传入文件名的情况下，往往网页链接会告诉我们
            final_path=os.path.join(save_dir,file_name)
        elif url.endswith('.gifv'):
            final_path = os.path.join(save_dir, file_name.replace('.gifv','.gif'))
        else:
            final_path = os.path.join(save_dir, file_name+'.jpg')
        # 如果没有显式指定后缀名，那么就用文件的链接后缀名做文件名
        # 这个方法不是很科学，但是一下也没有想到更好的办法，可以下载以后使用format_correction来进行校正

        if resume is None:
            resume=self.resume
        if min_size is None:
            min_size=self.min_size
        files_already_in=os.listdir(save_dir)
        # 用于检测是否已经存在同名文件
        if (not resume) and (not delete):
            counter=0
            while True:
                if (final_path.split('\\')[-1] in files_already_in) or (final_path.split('/')[-1] in files_already_in):
                    final_path=os.path.join(save_dir, file_name.replace('.jpg','')+str(counter)+'.jpg')
                    counter+=1
                    # 如果文件名已经存在了，那么就需要修改文件名，在文件名后面按顺序加0,1,2,3……
                else:
                    break

        if verbose:
            print(url)
            print('Saving to:',final_path)

        if delete:
            if os.path.isfile(final_path):
                os.remove(final_path)

        downloaded_size=0
        timeout_counter=0

        while True:
            try:
                with requests.get(url,headers=self.header,stream=True,) as x:
                    file_size=float(x.headers['Content-Length'])
                    if verbose:
                        print('File size %d kb'%(file_size//1024))
                        if file_size/1024<min_size:
                            print('The picture size is below %d. Will not download this picture.'%min_size)
                            break
                    if resume:
                        if os.path.isfile(final_path):
                            if (imghdr.what(final_path) is not None) and (os.path.getsize(final_path)==file_size):
                                # 文件大小正确，并且没有损坏
                                # 这是一个比较玄学的问题，因为只验证任何一方，都可能导致对已损坏文件的遗漏
                                if verbose:
                                    print('File already exists')
                                break

                    write_type='wb'
                    # 这个代码就比较容易理解
                    # 不论前面发生了什么，只要没有离开这个循环，那么下面肯定是要新建一个文件，从头开始了
                    # 所以这里直接规定按比特写即可

                    with open(final_path,write_type) as f:
                        for chunk in x.iter_content(chunk_size=5120*2):
                            f.write(chunk)
                            if verbose:
                                downloaded_size = downloaded_size + len(chunk)

                                process = (downloaded_size) / file_size * 100
                                sys.stdout.write('\r')
                                sys.stdout.write("%f%s" % (process, '%'))
                                sys.stdout.flush()
                break
            except urllib3.exceptions.ReadTimeoutError:
                print('\nTimeout, trying again')
                timeout_counter+=1
                if timeout_counter>3:
                    break
            except:
                traceback.print_exc()
                break


    def main(self):
        # 做了一个修改，避免创建一个文件夹以后不需要下载，导致创建空文件夹
        # 现在只有确认要下载以后，才会创建文件夹
        if not os.path.isdir(self.save_dir):
            # 如果这个路径不存在，那就创建这个路径
            os.makedirs(self.save_dir)

        if self.is_naver:
            self.url = sc.blog_naver(self.url).get_true_link()

        for src in self.request_page():
            if src is None:
                continue
            try:
                for keyword in self.nodownload_list:
                    if keyword in src:
                        raise pe.keyword_exception
            except pe.keyword_exception:
                continue

            if self.gif==False and 'gif' in src:
                # 对gif做一个判断
                continue
            pic=sc.is_tistory(src).return_url()
            # pic=sc.is_kpoping(pic).return_url()
            self.download_single_img(pic)

        print('Finishing download')
