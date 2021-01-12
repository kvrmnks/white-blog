import os
import subprocess


def copy_file(raw_path: str, target_path: str):
    raw_file = open(raw_path, 'rb')
    target_file = open(target_path, 'wb')
    content = raw_file.read()
    target_file.write(content)
    raw_file.close()
    target_file.close()


class Render:
    def __init__(self, markdown_location: str, html_location: str, web_template_location: str):
        self.markdown_location = markdown_location
        self.html_location = html_location
        self.web_template_location = web_template_location

        if not os.path.exists(html_location):
            os.makedirs(html_location)

        F = open(self.web_template_location, encoding='utf-8')
        self.web_template = F.read()
        F.close()

        self.web_title_cattle = '<!-- title -->'
        self.web_content_cattle = '<!-- <content> -->'

    def render_html_content(self, title: str, content: str) -> str:
        ret = self.web_template.replace(self.web_title_cattle, title, 1)
        ret = ret.replace(self.web_content_cattle, content, 1)
        return ret

    def render_markdown_html(self, markdown_path: str, html_path: str, title: str):
        f = open(markdown_path, 'r', encoding='utf-8')
        ret = subprocess.run(
            args=['hoedown', '--all-block', '--all-span', '--all-flags'],
            stdin=f,
            stdout=subprocess.PIPE,
            encoding='utf-8'
        )
        f.close()
        out_string = ret.stdout
        f_out = open(html_path, 'w', encoding='utf-8')
        f_out.write(self.render_html_content(title, out_string))
        f_out.close()
        print('finish render ' + markdown_path + ' to ' + html_path)

    def build_one_layer(self, markdown_path_layer: str, html_path_layer: str):
        if not os.path.exists(html_path_layer):
            os.makedirs(html_path_layer)
        dir_list = os.listdir(markdown_path_layer)

        # 处理markdown文件
        file_list = [i for i in dir_list if os.path.isfile(markdown_path_layer + '/' + i) and i.endswith(".md")]
        for i in file_list:
            cur_markdown_filename = markdown_path_layer + '/' + i
            cur_html_filename = html_path_layer + '/' + i.replace('.md', '.html')
            self.render_markdown_html(cur_markdown_filename, cur_html_filename, i.replace('.md', ''))

        # 处理其他文件 比如音乐或是视频
        file_list = [i for i in dir_list if os.path.isfile(markdown_path_layer + '/' + i) and (not i.endswith(".md"))]
        for i in file_list:
            cur_raw_filename = markdown_path_layer + '/' + i
            cur_html_filename = html_path_layer + '/' + i
            copy_file(cur_raw_filename, cur_html_filename)

    def build_next_layer(self, markdown_path_layer: str, html_path_layer: str):
        self.build_one_layer(markdown_path_layer, html_path_layer)
        dir_list = os.listdir(markdown_path_layer)
        dir_list = [i for i in dir_list if os.path.isdir(markdown_path_layer + '/' + i)]
        for i in dir_list:
            cur_markdown_layer_name = markdown_path_layer + '/' + i
            cur_html_layer_name = html_path_layer + '/' + i
            self.build_next_layer(cur_markdown_layer_name, cur_html_layer_name)

    def build(self):
        self.build_next_layer(self.markdown_location, self.html_location)
