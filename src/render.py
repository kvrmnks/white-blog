import os
import subprocess


def copy_file(raw_path: str, target_path: str):
    if os.path.isdir(raw_path):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            dl = os.listdir(raw_path)
            for x in dl:
                copy_file(raw_path+'/'+x, target_path+'/'+x)
    else:
        raw_file = open(raw_path, 'rb')
        target_file = open(target_path, 'wb')
        content = raw_file.read()
        target_file.write(content)
        raw_file.close()
        target_file.close()


def load_file(path: str) -> str:
    f = open(path, 'r', encoding='utf-8')
    ret = f.read()
    return ret


def save_file(path: str, content: str) -> None:
    f = open(path, 'w', encoding='utf-8')
    f.write(content)
    f.close()


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


def get_root_path(depth: int) -> str:
    ret = './'
    for i in range(depth):
        ret += '../'
    return ret


class Render:
    def __init__(self, user_config: dict,
                 system_config: dict
                 ):
        self.user_config = user_config
        self.system_config = system_config
        self.user_config['draft_output_location'] = self.user_config['output_location'] + '/draft'

        if not os.path.exists(self.user_config['output_location']):
            os.makedirs(self.user_config['output_location'])

        if not os.path.exists(self.user_config['draft_output_location']):
            os.makedirs(self.user_config['draft_output_location'])

        template_list = ['about_page_template',
                         'blog_page_template',
                         'card_template',
                         'home_page_template',
                         'normal_page_template']

        for x in template_list:
            self.system_config[x] = load_file(self.system_config[x])
            self.system_config[x] = self.system_config[x].replace(
                self.system_config['web_name_sh'],
                self.user_config['web_name']
            )
        self.blog_list = []
        self.draft_list = []

    def render_normal_page(self,
                           content: str,
                           cur_file: dict,
                           pr_file: dict,
                           nx_file: dict) -> str:
        ret = self.system_config['normal_page_template'].replace(self.system_config['blog_title_sh'], cur_file['title'])
        ret = ret.replace(self.system_config['content_sh'], content)
        partial_str = get_root_path(cur_file['depth'])
        ret = ret.replace(self.system_config['nav_home_sh'], partial_str + 'index.html')
        ret = ret.replace(self.system_config['nav_blog_sh'], partial_str + 'blog.html')
        ret = ret.replace(self.system_config['nav_about_sh'], partial_str + 'about.html')
        ret = ret.replace(self.system_config['global_css_sh'], partial_str + 'global.css')
        ret = ret.replace(self.system_config['global_js_sh'], partial_str + 'global.js')
        ret = ret.replace(self.system_config['normal_page_pre_page_name_sh'], pr_file['title'])
        ret = ret.replace(self.system_config['normal_page_pre_page_href_sh'], partial_str + pr_file['partial_path'])
        ret = ret.replace(self.system_config['normal_page_next_page_name_sh'], nx_file['title'])
        ret = ret.replace(self.system_config['normal_page_next_page_href_sh'], partial_str + nx_file['partial_path'])
        ret = ret.replace(self.system_config['favicon_href_sh'], partial_str + 'favicon.ico')
        return ret

    def render_abstract(self, markdown_path: str) -> str:
        # markdown_path 渲染的文件
        # 渲染一篇博客的摘要部分
        out_string = self.load_abstract_of_file(markdown_path)
        return render_markdown(out_string)

    def interpret_normal_page(self,
                              cur_file: dict,
                              pr_file: dict,
                              nx_file: dict):
        out_string = render_markdown(self.load_without_abstract_of_file(cur_file['file_path']))
        f_out = open(cur_file['out_partial_path'], 'w', encoding='utf-8')
        f_out.write(self.render_normal_page(out_string, cur_file, pr_file, nx_file))
        f_out.close()
        print('finish render ' + cur_file['file_path'] + ' to ' + cur_file['partial_path'])

    def load_abstract_of_file(self, path: str) -> str:
        # 加载文件的摘要部分
        file_content = load_file(path)
        abstract_cattle_location = file_content.find(self.system_config['blog_abstract_sh'])
        if abstract_cattle_location == -1:
            return ''
        else:
            return file_content[:abstract_cattle_location]

    def load_without_abstract_of_file(self, path: str) -> str:
        # 加载除去<!-- more -->的部分
        file_content = load_file(path)
        abstract_cattle_location = file_content.find(self.system_config['blog_abstract_sh'])
        if abstract_cattle_location == -1:
            return file_content
        else:
            return file_content[abstract_cattle_location + len(self.system_config['blog_abstract_sh']):]

    def render_card(self) -> str:
        # 生成关于卡片的html
        content = ''
        for x in self.blog_list:
            name = x['title']
            path = x['partial_parent_path'] + '/' + x['title'] + '.html'
            date = x['date']
            abstract = render_markdown(self.load_abstract_of_file(x['file_path']))
            if abstract == '':
                abstract = '阿巴阿巴, 这篇文章没写简介'

            partial_content = self.system_config['card_template'].replace(self.system_config['card_title_sh'], name)

            partial_content = partial_content.replace(self.system_config['card_content_sh'], abstract)
            partial_content = partial_content.replace(self.system_config['card_date_sh'], date)
            partial_content = partial_content.replace(self.system_config['card_href_sh'], path)
            content += partial_content
            content += '\n'
        content = self.system_config['blog_page_template'].replace(self.system_config['content_sh'], content)
        content = content.replace(self.system_config['nav_home_sh'], './index.html')
        content = content.replace(self.system_config['nav_blog_sh'], './blog.html')
        content = content.replace(self.system_config['nav_about_sh'], './about.html')
        content = content.replace(self.system_config['global_js_sh'], './global.js')
        content = content.replace(self.system_config['global_css_sh'], './global.css')
        return content

    def interpret_blog_list_page(self):
        # 由于需要每个blog的具体地址，需要先构建文件再构造链接
        # 生成blog界面的各个链接
        self.blog_list.sort(key=lambda x: x['date'])
        self.blog_list.reverse()
        blog_file = open(self.user_config['output_location'] + '/blog.html', 'w', encoding='utf-8')
        blog_file.write(self.render_card().replace(self.system_config['favicon_href_sh'], './favicon.ico'))
        blog_file.close()

    def build_js_and_css(self):
        copy_file(self.system_config['global_js'], self.user_config['output_location'] + '/global.js')
        copy_file(self.system_config['global_css'], self.user_config['output_location'] + '/global.css')

    def build_about_and_home_page(self):
        home_page = self.system_config['home_page_template']
        about_page = self.system_config['about_page_template']
        nav_sh_list = ['nav_about_sh', 'nav_home_sh', 'nav_blog_sh']
        nav_list = ['./about.html', './index.html', './blog.html']

        for i in range(len(nav_sh_list)):
            home_page = home_page.replace(self.system_config[nav_sh_list[i]], nav_list[i])
            about_page = about_page.replace(self.system_config[nav_sh_list[i]], nav_list[i])

        home_page_md = load_file(self.user_config['home_page_location'])
        about_page_md = load_file(self.user_config['about_page_location'])

        home_page = home_page.replace(self.system_config['content_sh'], render_markdown(home_page_md))
        about_page = about_page.replace(self.system_config['content_sh'], render_markdown(about_page_md))

        home_page = home_page.replace(self.system_config['web_title_sh'], 'Home')
        about_page = about_page.replace(self.system_config['web_title_sh'], 'About')

        home_page = home_page.replace(self.system_config['global_js_sh'], './global.js')
        home_page = home_page.replace(self.system_config['global_css_sh'], './global.css')

        about_page = about_page.replace(self.system_config['global_js_sh'], './global.js')
        about_page = about_page.replace(self.system_config['global_css_sh'], './global.css')

        home_page = home_page.replace(self.system_config['favicon_href_sh'], './favicon.ico')
        about_page = about_page.replace(self.system_config['favicon_href_sh'], './favicon.ico')

        save_file(self.user_config['output_location'] + './index.html', home_page)
        save_file(self.user_config['output_location'] + './about.html', about_page)

    def search_markdown(self,
                        log: list,
                        depth: int,
                        partial_parent_path: str,
                        date: str,
                        path: str) -> None:
        dir_list = os.listdir(path)

        file_list = [i for i in dir_list if os.path.isfile(path + '/' + i) and i.endswith('.md')]
        dir_list = [i for i in dir_list if os.path.isdir(path + '/' + i)]

        for x in dir_list:
            tmp = date
            if depth == 1:
                tmp = x
            if 1 < depth <= 3:
                tmp = date + '.' + x
            self.search_markdown(log, depth + 1, partial_parent_path + '/' + x, tmp, path + '/' + x)

        for x in file_list:
            log.append({
                'title': x.replace('.md', ''),
                'file_path': path + '/' + x,
                'file_parent_path': path,
                'partial_parent_path': partial_parent_path,
                'partial_path': partial_parent_path + '/' + x.replace('.md', '.html'),
                'date': date,
                'depth': depth
            })

    def search_all_blog(self):
        for x in self.user_config['blog_location']:
            self.search_markdown(self.blog_list, 1, '.', '', x)
        length = len(self.blog_list)
        for x in range(length):
            df = self.user_config['output_location'] + '/'
            self.blog_list[x]['out_partial_parent_path'] = df + self.blog_list[x]['partial_parent_path']
            self.blog_list[x]['out_partial_path'] = df + self.blog_list[x]['partial_path']
        # print(self.blog_list)

    def search_all_draft(self):
        for x in self.user_config['draft_location']:
            self.search_markdown(self.draft_list, 1, '.', '', x)
        length = len(self.draft_list)
        for x in range(length):
            self.draft_list[x]['depth'] += 1
            df = self.user_config['draft_output_location'] + '/'

            self.draft_list[x]['out_partial_parent_path'] = df + self.draft_list[x]['partial_parent_path']
            self.draft_list[x]['out_partial_path'] = df + self.draft_list[x]['partial_path']
            self.draft_list[x]['partial_path'] = './draft/' + self.draft_list[x]['partial_path']
        # print(self.draft_list)

    def build_all_blog(self):
        self.move_all_blog_file()
        self.render_all_blog()

    def build_all_draft(self):
        self.move_all_draft_file()
        self.render_all_draft()

    def move_all_blog_file(self):
        for x in self.blog_list:
            files = os.listdir(x['file_parent_path'])
            files = [i for i in files if (not i.endswith('.md'))]
            # print(files)
            output_str = self.user_config['output_location'] + '/' + x['partial_parent_path']
            if not os.path.exists(output_str):
                os.makedirs(output_str)
            for y in files:
                copy_file(x['file_parent_path'] + '/' + y, output_str + '/' + y)

    def move_all_draft_file(self):
        for x in self.draft_list:
            files = os.listdir(x['file_parent_path'])
            files = [i for i in files if not i.endswith('.md')]
            output_str = self.user_config['draft_output_location'] + '/' + x['partial_parent_path']
            if not os.path.exists(output_str):
                os.makedirs(output_str)
            for y in files:
                copy_file(x['file_parent_path'] + '/' + y, output_str + '/' + y)

    def render_list(self, d: list):
        length = len(d)
        for x in range(length):
            nx_file = d[(x + 1) % length]
            pr_file = d[(x - 1 + length) % length]
            cur_file = d[x]
            self.interpret_normal_page(cur_file, pr_file, nx_file)

    def render_all_blog(self):
        self.render_list(self.blog_list)

    def render_all_draft(self):
        self.render_list(self.draft_list)

    def build(self):
        self.build_favicon()
        self.build_js_and_css()
        self.build_about_and_home_page()

        self.search_all_blog()
        self.search_all_draft()

        self.interpret_blog_list_page()

        self.build_all_blog()
        self.build_all_draft()
        # print(self.draft_list)

    def build_favicon(self):
        copy_file(self.system_config['favicon_location'], self.user_config['output_location'] + '/favicon.ico')
