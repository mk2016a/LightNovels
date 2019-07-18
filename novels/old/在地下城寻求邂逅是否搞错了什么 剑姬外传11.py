import sys
sys.path.append('.')

from novels.core.epub_make import *

# Chapter Pattern
## Numbers
re_number = '[1234567890０１２３４５６７８９一二三四五六七八九十百①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]{1,5}?'
## chapter title split pattern core
chapter_pattern_core = ('(幕间)|(序言)|(目录)|(间章)|(尾声)|'
         '('+re_number+'章)')
## chapter title split pattern
chapter_pattern = '(?im)(?<=<strong>)('+chapter_pattern_core+')[^<>]{0,20}?(?=</strong>)'


# Epub Make
uris = [
    'https://tieba.baidu.com/p/6005357137',             #   剑姬外传 11卷 插画
    'https://tieba.baidu.com/p/6014940237?see_lz=1',    #   外传11卷 序章 试翻
    'https://tieba.baidu.com/p/6015134196?see_lz=1',    #   外传11卷 第一章 试翻
    'https://tieba.baidu.com/p/6016156666?see_lz=1',    #   外传11卷 第二章 决战之际 试翻
    'https://tieba.baidu.com/p/6019030639?see_lz=1',	#   外传11卷 第三章 神の素顔 试翻
    'https://tieba.baidu.com/p/6021653518?see_lz=1',	#   外传11卷 第四章 库诺索斯战役 试翻
    'https://tieba.baidu.com/p/6033903657?see_lz=1',    #	外传11卷 第五章 迷执显现 试翻'
    'https://tieba.baidu.com/p/6038296645?see_lz=1',    #	外传11卷 第六章 『之后，神明展露笑颜』 试翻'
    'https://tieba.baidu.com/p/6049972892?see_lz=1',    #   外传11卷 尾声Epilogue Whodunit 试翻
       ]
#epub_make(uris, '11 bd', chapter_check=False)
uris = 'https://www.lightnovel.cn/thread-956865-1-1.html'
epub_make(uris, '11 ln', chapter_check=True, chapter_pattern=chapter_pattern)