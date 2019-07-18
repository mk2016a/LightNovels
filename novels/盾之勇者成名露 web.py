import sys
sys.path.append('.')

from novels.core.epub_make import *

# Numbers
# chapter title split pattern core
chapter_pattern_core = ('([间终]\s{0,5}?章)|'
         '(第\s{0,3}?'+re_number+'\s{0,3}?[章话节])|'
         '((?<=\W)'+re_number+'\s{0,3}?[章话节])|'
         '('+re_number+'[\.\s])|'
         '('+re_number+'(?=<))|'
         '(web.{0,5}?'+re_number+')|'
         '((Chapter)|(CH).{0,5}?'+re_number+')|'
         '((?<=\W)序幕)|(?<=\W)(尾声)|(?<=\W)(后记)|(?<=\W)(目录)|(?<=\W)(Epilogue)|(?<=\W)(CONTENTS)|(?<=\W)(角色介绍)|(?<=\W)(幕间)')
# chapter title split pattern
chapter_pattern = '(?im)[^<>]{0,10}?('+chapter_pattern_core+')[^<>完鞍]{0,30}?(?=<)'


uris = [
    '/Volumes/Storage/Downloads/盾之勇者成名路 Web.epub',
    '/Volumes/Storage/Downloads/486～505-20190425T050542Z-001.zip',
    #'https://tieba.baidu.com/p/6015916116?see_lz=1',        # 486~505
    'https://tieba.baidu.com/p/6015572584',     # 506
    'https://tieba.baidu.com/p/6015872682',     # 507
    'https://tieba.baidu.com/p/6016520655',     # 508
    'https://tieba.baidu.com/p/6018636805',     # 509
    'https://tieba.baidu.com/p/6020220249',     # 510
    'https://tieba.baidu.com/p/6022022252',     # 511
    'https://tieba.baidu.com/p/6022121748',     # 512
    'https://tieba.baidu.com/p/6024283538',     # 513
    'https://tieba.baidu.com/p/6025357453',     # 514
    'https://tieba.baidu.com/p/6032838554',     # 515
    'https://tieba.baidu.com/p/6034426612',     # 516
    'https://tieba.baidu.com/p/6035422707',     # 517
    'https://tieba.baidu.com/p/6039962158',     # 518
    'https://tieba.baidu.com/p/6044003906',     # 519
    'http://tieba.baidu.com/p/6047348249',      # 520
    'http://tieba.baidu.com/p/6048513989',      # 521
    'https://tieba.baidu.com/p/6073368786?see_lz=1',    # 522
    'https://tieba.baidu.com/p/6073579756?see_lz=1',    # 523
    'https://tieba.baidu.com/p/6073727589?see_lz=1',    # 524
    'https://tieba.baidu.com/p/6074518850?see_lz=1',    # 525
    'https://tieba.baidu.com/p/6074677781?see_lz=1',    # 526
    'https://tieba.baidu.com/p/6081506442?see_lz=1',    # 527
    'https://tieba.baidu.com/p/6081611286?see_lz=1',    # 528
    'https://tieba.baidu.com/p/6083166513',             # 529
    'https://tieba.baidu.com/p/6086881191',             # 530
    'https://tieba.baidu.com/p/6086947769?see_lz=1',    # 531
    'https://tieba.baidu.com/p/6090251353?see_lz=1',    # 532
    'https://tieba.baidu.com/p/6090345451?see_lz=1',    # 533
    'https://tieba.baidu.com/p/6113224065',             # 534
    'https://tieba.baidu.com/p/6113224065',         # 534
    'https://tieba.baidu.com/p/6122617138',  # 535
    'https://tieba.baidu.com/p/6122897696',  # 536
    'https://tieba.baidu.com/p/6122964366',  # 537
    'https://tieba.baidu.com/p/6126862838',  # 538
    'https://tieba.baidu.com/p/6127005861',  # 539
    'https://tieba.baidu.com/p/6139231568?see_lz=1',    # 540

]
#epub_make(uris=uris, book_title='盾之勇者成名路 Web', chapter_check=True, chapter_pattern=chapter_pattern, time_stamp=False)


uris = [
    '/Volumes/Storage/Mine/Novels/盾之勇者成名录/盾之勇者成名路 Web.epub',
    #'https://tieba.baidu.com/p/6147345339',         # 541
]
epub_make(uris=uris, book_title='盾之勇者成名路 Web', chapter_check=False, time_stamp=False)