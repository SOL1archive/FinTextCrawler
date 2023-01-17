def get_listed(item):
    if type(item) != list:
        item = [item]

    return item

def delay(option):
    import time
    sleep_time = -1
    if type(option) == str:
        if option.isnumeric():
            sleep_time = float(option)
        elif option == 'Normal Dist':
            import numpy as np
            while sleep_time < 0.2:
                sleep_time = np.random.normal(loc=0.5)
        else:
            raise RuntimeError
    elif type(option) == int or type(option) == float:
        sleep_time = option
    
    time.sleep(sleep_time)

def append_dict(target_dict : dict, source_dict):
    import copy

    if source_dict == None:
        return target_dict
    
    target_dict = copy.deepcopy(target_dict)
    for source_key in source_dict.keys():
        target_dict[source_key] = source_dict[source_key]

    return target_dict

def url_query(base_url, query_dict):
    base_url = base_url + '?'
    for key in query_dict.keys():
        base_url = base_url + key + '=' + str(query_dict[key]) + '&'
    
    return base_url[:-1]

def next_token_queue(token_queue, response, keyword):
    import json
    if not json.loads(response.text)['meta'].get('next_token', True):
        token_queue.append((keyword, response['meta']['next_token']))

def check_status_code(response):
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

def None2null(value):
    return 'null' if value == None else value

def make_escape_seq(value):
    import re
    string = str(value)
    return re.sub('\"', r'\"', string)

def datetime_json_default(value):
    import datetime
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return value

def dump_json(article, filename):
    import json

    with open(filename, 'a', encoding='UTF-8') as f:
        article_json = json.dumps(article, default=datetime_json_default)
        f.write(article_json)
        