import test_parse
import simply_measured
import climate_corp
import redfin
import random_people

import re

my_url = ['http://www.linkedin.com/in/dleen']

company_urls = [
    my_url,
    simply_measured.simply_measured_urls,
    climate_corp.climate_corp_urls,
    redfin.redfin_urls,
    random_people.random_urls
]


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
        user_page = test_parse.linked_parse(u)
        user_page = user_page['hresume'][0]
        user_features = user_items(user_page)
        user_string = ' '.join(user_features)

        f_out.write('%d %s\n' % (id, user_string))


f = open('people.txt', 'w')

for i, u in enumerate(company_urls, start=0):
    write_linkedin_data(f, i, u)

f.close()


# for n, u in zip(simply_measured.simply_measured_people,
#                 simply_measured.simply_measured_urls):
#     print u
#     user_page = test_parse.linked_parse(u)
#     user_page = user_page['hresume'][0]
#     user_features = user_items(user_page)
#     user_string = ' '.join(user_features)

#     f.write('%d %s\n' % (1, user_string))

# for n, u in zip(climate_corp.climate_corp_people,
#                 climate_corp.climate_corp_urls):
#     print u
#     user_page = test_parse.linked_parse(u)
#     user_page = user_page['hresume'][0]
#     user_features = user_items(user_page)
#     user_string = ' '.join(user_features)

#     f.write('%d %s\n' % (2, user_string))

# for u in random_people.random_urls:
#     print u
#     user_page = test_parse.linked_parse(u)
#     user_page = user_page['hresume'][0]
#     user_features = user_items(user_page)
#     user_string = ' '.join(user_features)

#     f.write('%d %s\n' % (0, user_string))

