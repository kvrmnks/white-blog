import render

if __name__ == '__main__':
    r = render.Render(r'../docs',
                      r'../site',
                      './template/web_template.html',
                      './template/blog_template.html',
                      './template/card_template.html',
                      './css/global.css',
                      './javascript/global.js',
                      "Kvrmnks' blog")
    # r.render_markdown_content('dsfsdfsdfsd')
    r.build()
    print(r.blog_list)
