class redownload_exception(Exception):
    def __init__(self):
        '''
        :param error_info:错误信息，这里直接传入了
        '''
        self.error_info='这个网页已经被日志记录过，不再进行爬取'
        Exception.__init__(self)

    def __str__(self):
        '''
        字符串，用于在print中输出信息
        :return:
        '''
        return self.error_info

class keyword_exception(Exception):
    def __init__(self):
        '''
        :param error_info:错误信息，这里直接传入了
        '''
        self.error_info='出现了不希望被爬取的关键字，跳过这个图片'
        Exception.__init__(self)

    def __str__(self):
        '''
        字符串，用于在print中输出信息
        :return:
        '''
        return self.error_info

class pic_no_found_error(Exception):
    def __init__(self):
        self.error_info='此网页中没有找到图片'
        Exception.__init__(self)

    def __str__(self):
        return self.error_info

class delete_exception(Exception):
    def __init__(self):
        '''
        :param error_info:错误信息，这里直接传入了
        '''
        self.error_info='不能删除自身所在的文件夹！'
        Exception.__init__(self)
    def __str__(self):
        return self.error_info

class folder_file_exists_exception(Exception):
    def __init__(self):
        '''
        :param error_info:错误信息，这里直接传入了
        '''
        self.error_info='这个文件夹/文件已经存在且未被要求删除，请检查文件夹或代码'
        Exception.__init__(self)

    def __str__(self):
        '''
        字符串，用于在print中输出信息
        :return:
        '''
        return self.error_info

class url_error(Exception):
    def __init__(self):
        '''
        :param error_info:错误信息，这里直接传入了
        '''
        self.error_info='未传入合适的链接，请检查输入'
        Exception.__init__(self)

    def __str__(self):
        '''
        字符串，用于在print中输出信息
        :return:
        '''
        return self.error_info