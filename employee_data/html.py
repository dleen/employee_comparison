from bs4 import BeautifulSoup
import json
import collections
import re


f = open('data/simply/chrisc.html', 'r').read()

id = 'top_card-content'
doc = BeautifulSoup(f)

j = doc.find_all('code')
print len(j)


def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)

tot_dict = {}

for l in j:
    print type(l.string)
    print l.string[0:100]
    print l.string[-20:]
    # print l.string
    jjj = json.loads(l.string)
    # fd = flatten(jjj)
    # tot_dict.update(fd)

# for k, v in tot_dict.iteritems():
#     #         all([False for x in [] if x in v])):
#     if type(v) == list and v:
#         # test = json.loads(v[0])
#         # print k
        # tot_dict.update(v[0])

# for k, v in tot_dict['content_TopCard_positionsMpr_topPrevious'][0].iteritems():
#     print k, v


