import linkedin_parser as lp
import re


def user_items(d):
    items = []
    if isinstance(d, dict):
        for _, v in d.iteritems():
            items.extend(user_items(v))
    elif isinstance(d, list):
        for v in d:
            items.extend(user_items(v))
    elif isinstance(d, basestring):
        items.extend(re.findall('\w{3}\w+', d))
    else:
        print type(d), d

    items = [x.lower() for x in items]
    return items


def write_linkedin_data(f_out, id, urls):
    for u in urls:
        print u
        user_page = lp.linked_parse(u)
        user_page = user_page['hresume'][0]
        user_features = user_items(user_page)
        user_features = \
            [x for x in user_features if len(x) < 20]
        user_string = ' '.join(user_features)

        f_out.write('%d %s\n' % (id, user_string))
