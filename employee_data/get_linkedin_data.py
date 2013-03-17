import test_parse
import collections


simply_measured_people = [
    'Adam Schoenfeld',
    'Damon Cortesi',
    'Otis Kimzey',
    'Lauren Berry',
    'Katie Ferris',
    'Heather Dooley',
    'Colin Henry',
    'Nathan Smitha',
    'Daniel Worthington',
    'Chris Castle',
    'Jon Culver',
    'Gino Valente',
    'Annette Auger',
    'Brian McGehee',
    'Meagan Johnston'
]

simply_measured_urls = [
    'http://www.linkedin.com/in/adamschoenfeld',
    'http://www.linkedin.com/in/dacort',
    'http://www.linkedin.com/in/otiskimzey',
    'http://www.linkedin.com/in/alaurenberry',
    'http://www.linkedin.com/in/katieferris',
    'http://www.linkedin.com/in/heatherdooley',
    'http://www.linkedin.com/in/jchenry',
    'http://www.linkedin.com/in/nathansmitha',
    'http://www.linkedin.com/in/halffullheart',
    'http://www.linkedin.com/in/crcastle',
    'http://www.linkedin.com/in/jonculver',
    'http://www.linkedin.com/in/ginovalente',
    'http://www.linkedin.com/in/annetteauger',
    'http://www.linkedin.com/in/brianmcgehee',
    'http://www.linkedin.com/in/mjohnston'
]

# for n, u in zip(simply_measured_people, simply_measured_urls):
#     print n
#     print test_parse.linked_parse(u)


def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        elif type(v) == list:
            new_list_key = new_key + '_'
            for i, lv in enumerate(v):
                print i, lv
                if isinstance(lv, collections.MutableMapping):
                    items.extend(flatten(lv, new_list_key).items())
                else:
                    items.append((new_list_key + lv.keys(), lv.items()))
        else:
            items.append((new_key, v))
    return dict(items)


y = test_parse.linked_parse('http://www.linkedin.com/in/katieferris')
y = y['hresume'][0]

# for i, v in enumerate(y['affiliation']):
#     print i, v


# for k, v in y.iteritems():
#     print k, v

z = flatten(y)

for k, v in z.iteritems():
    print k, v

# print z.viewvalues()
