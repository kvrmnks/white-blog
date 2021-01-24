import os
import subprocess


def copy_file(raw_path: str, target_path: str):
    raw_file = open(raw_path, 'rb')
    target_file = open(target_path, 'wb')
    content = raw_file.read()
    target_file.write(content)
    raw_file.close()
    target_file.close()


def load_file(path: str) -> str:
    F = open(path, 'r', encoding='utf-8')
    ret = F.read()
    return ret


def render_markdown(content: str) -> str:
    ret = subprocess.Popen(
        args=['./module/hoedown.exe', '--all-block', '--all-span', '--all-flags'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    ret.stdin.write(content)
    ret.stdin.close()
    string_lines = ret.stdout.readlines()
    out = ''
    for i in string_lines:
        out += i
    return out


class Render:
    def __init__(self, markdown_location: str,
                 html_location: str,
                 web_template_location: str,
                 blog_template_location: str,
                 card_template_location: str,
                 global_css_location: str,
                 global_js_location: str,
                 web_name: str):
        self.markdown_location = markdown_location
        self.html_location = html_location
        self.web_template_location = web_template_location
        self.blog_template_location = blog_template_location
        self.card_template_location = card_template_location
        self.global_js_location = global_js_location
        self.global_css_location = global_css_location
        self.blog_list = []

        if not os.path.exists(html_location):
            os.makedirs(html_location)

        # 加载模板
        self.web_template = load_file(self.web_template_location)
        self.blog_template = load_file(self.blog_template_location)
        self.card_template = load_file(self.card_template_location)

        # 加载占位符
        self.web_title_cattle = '<!-- title -->'
        self.web_content_cattle = '<!-- <content> -->'
        self.blog_content_cattle = '<!-- <content> -->'

        self.card_title_cattle = '<!-- title -->'
        self.card_content_cattle = '<!-- content -->'
        self.card_date_cattle = '<!-- date -->'
        self.card_href_cattle = '<!-- href -->'

        self.web_abstract_cattle = '<!-- more -->'
        self.web_name_cattle = '<!-- web-name -->'

        self.nav_home_cattle = '<!-- nav-home-href -->'
        self.nav_blog_cattle = '<!-- nav-blog-href -->'
        self.nav_about_cattle = '<!-- nav-about-href -->'

        self.global_css = '<!-- global-css -->'
        self.global_js = '<!-- global-js -->'

        self.web_template = self.web_template.replace(self.web_name_cattle, web_name)
        self.blog_template = self.blog_template.replace(self.web_name_cattle, web_name)

    def render_web_page(self, title: str, content: str, depth: int) -> str:
        ret = self.web_template.replace(self.web_title_cattle, title, 1)
        ret = ret.replace(self.web_content_cattle, content, 1)
        partial_str = './'
        for i in range(depth):
            partial_str += '../'
        ret = ret.replace(self.nav_home_cattle, partial_str + 'index.html')
        ret = ret.replace(self.nav_blog_cattle, partial_str + 'blog.html')
        ret = ret.replace(self.nav_about_cattle, partial_str + 'about.html')
        ret = ret.replace(self.global_css, partial_str + 'global.css')
        ret = ret.replace(self.global_js, partial_str + 'global.js')
        return ret

    def render_abstract(self, markdown_path: str) -> str:
        # markdown_path 渲染的文件
        # 渲染一篇博客的摘要部分
        out_string = self.load_abstract_of_file(markdown_path)
        return render_markdown(out_string)

    def interpret_web_page(self, markdown_path: str, html_path: str, title: str, depth: int):
        out_string = render_markdown(self.load_without_abstract_of_file(markdown_path))
        f_out = open(html_path, 'w', encoding='utf-8')
        f_out.write(self.render_web_page(title, out_string, depth))
        f_out.close()
        print('finish render ' + markdown_path + ' to ' + html_path)

    def load_abstract_of_file(self, path: str) -> str:
        # 加载文件的摘要部分
        file_content = load_file(path)
        abstract_cattle_location = file_content.find(self.web_abstract_cattle)
        if abstract_cattle_location == -1:
            return ''
        else:
            return file_content[:abstract_cattle_location]

    def load_without_abstract_of_file(self, path: str) -> str:
        # 加载除去<!-- more -->的部分
        file_content = load_file(path)
        abstract_cattle_location = file_content.find(self.web_abstract_cattle)
        if abstract_cattle_location == -1:
            return file_content
        else:
            return file_content[abstract_cattle_location + len(self.web_abstract_cattle):]

    def build_one_layer(self, markdown_path_layer: str,
                        html_path_layer: str,
                        partial_location: str,
                        depth: int,
                        date: str):

        # markdown_path_layer 正在解析的地址
        # html_path_layer 正在生成的地址
        # partial_location 相对位置
        # depth 相对位置中的层数
        # date 用于生成blog的时间

        if not os.path.exists(html_path_layer):
            os.makedirs(html_path_layer)
        dir_list = os.listdir(markdown_path_layer)

        # 处理markdown文件
        file_list = [i for i in dir_list if os.path.isfile(markdown_path_layer + '/' + i) and i.endswith(".md")]

        for i in file_list:
            cur_markdown_filename = markdown_path_layer + '/' + i
            cur_html_filename = html_path_layer + '/' + i.replace('.md', '.html')
            self.interpret_web_page(cur_markdown_filename, cur_html_filename, i.replace('.md', ''), depth)
            if depth != 0:
                self.blog_list.append({
                    'title': i.replace('.md', ''),
                    'path': partial_location + '/' + i.replace('.md', '.html'),
                    'date': date,
                    'abstract': self.render_abstract(cur_markdown_filename)
                })

        # 处理其他文件 比如音乐或是视频
        file_list = [i for i in dir_list if os.path.isfile(markdown_path_layer + '/' + i) and (not i.endswith(".md"))]
        for i in file_list:
            cur_raw_filename = markdown_path_layer + '/' + i
            cur_html_filename = html_path_layer + '/' + i
            copy_file(cur_raw_filename, cur_html_filename)

    def build_next_layer(self, markdown_path_layer: str,
                         html_path_layer: str,
                         partial_location: str,
                         depth: int,
                         date: str):
        # markdown_path_layer 正在解析的地址
        # html_path_layer 正在生成的地址
        # partial_location 相对位置
        # depth 相对位置中的层数
        # date 用于生成blog的时间
        self.build_one_layer(markdown_path_layer, html_path_layer, partial_location, depth, date)
        dir_list = os.listdir(markdown_path_layer)
        dir_list = [i for i in dir_list if os.path.isdir(markdown_path_layer + '/' + i)]
        for i in dir_list:
            cur_markdown_layer_name = markdown_path_layer + '/' + i
            cur_html_layer_name = html_path_layer + '/' + i
            cur_data = date
            if 1 == depth:
                cur_data = i
            if 1 < depth <= 3:
                cur_data += '.' + i
            self.build_next_layer(cur_markdown_layer_name,
                                  cur_html_layer_name,
                                  partial_location + '/' + i,
                                  depth + 1,
                                  cur_data)

    def render_card(self) -> str:
        # 生成关于卡片的html
        content = ''
        for x in self.blog_list:
            name = x['title']
            path = x['path']
            date = x['date']
            abstract = x['abstract']
            if abstract == '':
                abstract = '阿巴阿巴, 这篇文章没写简介'

            partial_content = self.card_template.replace(self.card_title_cattle, name)

            partial_content = partial_content.replace(self.card_content_cattle, abstract)
            partial_content = partial_content.replace(self.card_date_cattle, date)
            partial_content = partial_content.replace(self.card_href_cattle, path)
            content += partial_content
            content += '\n'
        content = self.blog_template.replace(self.blog_content_cattle, content)
        content = content.replace(self.nav_home_cattle, './index.html')
        content = content.replace(self.nav_blog_cattle, './blog.html')
        content = content.replace(self.nav_about_cattle, './about.html')
        content = content.replace(self.global_js, './global.js')
        content = content.replace(self.global_css, './global.css')
        return content

    def interpret_blog_page(self):
        # 由于需要每个blog的具体地址，需要先构建文件再构造链接
        # 生成blog界面的各个链接
        self.blog_list.sort(key=lambda x: x['date'])
        self.blog_list.reverse()
        blog_file = open(self.html_location + '/blog.html', 'w', encoding='utf-8')
        blog_file.write(self.render_card())
        blog_file.close()

    def build_js_and_css(self):
        copy_file(self.global_js_location, self.html_location + '/global.js')
        copy_file(self.global_css_location, self.html_location + '/global.css')

    def build(self):
        self.build_js_and_css()
        self.build_next_layer(self.markdown_location, self.html_location, '.', 0, '')
        self.interpret_blog_page()
