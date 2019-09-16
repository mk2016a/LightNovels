from novels.core.epub_core import *
import csv

def getList(url, folder = download_dir):
    soup = bsoup(url)
    contents = soup.find_all(class_='d_post_content j_d_post_content ')
    all_content = ''
    for content in contents:
        all_content += str(content)

    index_list = []
    results = re.findall('(?<=</a>)(.+?)<a.+?>(.+?)</a>', all_content)
    for result in results:
        if re.match('https?://tieba.baidu.com', result[1]):
            result0 = re.sub('(<.*?>)|(\s)', '', result[0])
            index_list.append((result0, result[1]))
    print(index_list)

    file = folder+'url_list.csv'
    with open(file, 'w+') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(('title', 'url'))
        for row in index_list:
            csv_write.writerow(row)

    print(file)
