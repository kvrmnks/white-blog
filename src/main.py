import render
import json

if __name__ == '__main__':
    user_config_file = open('./user_config.json', 'r', encoding='utf-8')
    system_config_file = open('./system_config.json', 'r', encoding='utf-8')
    user_json = json.loads(user_config_file.read())
    system_json = json.loads(system_config_file.read())

    user_config_file.close()
    system_config_file.close()

    r = render.Render(
        user_json,
        system_json
    )
    r.build()
    # print(r.blog_list)
