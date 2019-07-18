from novels.core.epub_core import *

txt_replacements = [
    ('\r', '\n'),
    (r'&#160;', ''),
    (r'&nbsp;', ''),
    ('<', '&gt;'),
    ('>', '&lt;'),
    ('(?m).+', '<p>\g<0></p>'),
]

class Epub_Txt():
    def __init__(self, files, chapter_check=False, codes=''):
        # Files
        if isinstance(files, str):
            self.files = [files]
        self.chapter_check = chapter_check
        # Codecs
        if isinstance(codes, list):
            self.codes = codes
        elif isinstance(codes, str) and codes != '':
            self.codes = [codes]
        else:
            self.codes = ['utf-8', 'gbk', 'utf-16']
        # Title and Content
        self.title = files[0].split('/')[-1].split('.')[0]
        self.getContent()

    def getContent(self):
        files = self.files
        codes = self.codes
        title_content = []
        for file in files:
            print(file)
            title = file.split('/')[-1].split('.')[0]
            for code in codes:
                try:
                    with open(file, 'r', encoding=code) as f:
                        content = f.read()
                        content = modify_txt(content)
                        content = convert_chinese(content)
                        break
                except Exception as e:
                    pass
            print(content)
            title_content.append((title, content))
        self.title_content = title_content

        return title_content


    def make_epub(self, chapter_pattern=chapter_pattern, second_pattern=second_pattern):
        #prepare
        print('Making Epub...')
        file = self.files[0].split('.')[0]+'.epub'
        title = self.title
        title_content = self.title_content
        check_delete_file(file)
        book = mkepub.Book(title)
        if self.chapter_check:
            for title, content in title_content:
                chapters = double_split(title, content, chapter_pattern, second_pattern)
                addChapter(book, title, chapters)
        else:
            for title, content in title_content:
                book.add_page(title, content)
        book.set_stylesheet(css_data)
        book.save(file)
        print(file)

def modify_txt(content, replacements=txt_replacements):
    for (old, new) in replacements:
        content = re.sub(old, new, content, flags=re.M)
    return content


def get_files(pattern, folder='/Volumes/Storage/Downloads'):
    file_list = []
    for root, folders, files in os.walk(folder):
        for file in files:
            if re.search(pattern, file):
                path = root+'/'+file
                file_list.append(path)
                print(path)
    return file_list

