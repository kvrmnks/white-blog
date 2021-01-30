import render
import json

if __name__ == '__main__':
    config_file = open('./config.json', 'r')
    js = json.loads(config_file.read())
    print(js)
    config_file.close()
    r = render.Render(
        js,
        './template/web_template.html',
        './template/blog_template.html',
        './template/card_template.html',
        './css/global.css',
        './javascript/global.js',
    )
    r.build()
    print(r.blog_list)
