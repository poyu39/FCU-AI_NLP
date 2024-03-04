# -*- coding:utf-8 -*-
# Author：hankcs
# Date: 2018-05-24 22:11
# 《自然語言處理入門》2.2.2 詞典的載入
# 配套書籍：http://nlp.hankcs.com/book.php
# 討論答疑：https://bbs.hankcs.com/
from pyhanlp import *


def load_dictionary():
    """
    載入HanLP中的mini詞庫
    :return: 一個set形式的詞庫
    """
    IOUtil = JClass('com.hankcs.hanlp.corpus.io.IOUtil')
    path = HanLP.Config.CoreDictionaryPath.replace('.txt', '.mini.txt')
    dic = IOUtil.loadDictionary([path]) # type: ignore
    return set(dic.keySet())


if __name__ == '__main__':
    dic = load_dictionary()
    print(len(dic))
    print(list(dic)[0])
