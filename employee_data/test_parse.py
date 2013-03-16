"""
Model for microformat properties and parsers. A microformat parser can
parse an HTML element into a dictionary of properties, whose keys are
strings and whose values are strings or other dictionary of properties.

As an example, the main program of this script parses an hResume from
given URL.
"""

import pprint
import re
import urllib
import urllib2
import urlparse
from cStringIO import StringIO

import html5lib
import lxml.html


class BaseMicroformatProperty(object):
    """ Base class for a microformat property """

    def __init__(self, root, index=0):
        self.root = root
        self.index = index  # None for multiple values, else selects one

    def parse(self, node):
        children = self.get_children(node)

        if children is None:
            return {}
        if self.index is None:
            value = filter(
                lambda value: value is not None,
                [self.get_value(child) for child in children]) or None
        else:
            try:
                child = children[self.index]
            except IndexError:
                value = None
            else:
                value = self.get_value(child)
        return {self.get_key(): value} if value is not None else {}

    def get_children(self, node):
        return node.find_class(self.root)

    def get_key(self):
        return self.root

    def get_value(self, node):
        mapper = {'abbr': ('title',), 'a': ('href', 'alt'),
                  'img': ('src',), 'object': ('data',)}
        value = None
        for attr in mapper.get(node.tag, []):
            if attr in node.attrib:
                value = node.attrib[attr]
                break
        if value is None:
            value = node.text_content()
        return self.transform_value(value)

    def transform_value(self, value):
        return force_unicode(whitespace_cleanup(value))


class NestingMicroformatProperty(BaseMicroformatProperty):
    """ Base class for a microformat property that can have other nested """

    def __init__(self, root, index=0, subproperties=None):
        super(NestingMicroformatProperty, self).__init__(root, index)
        self.subproperties = subproperties or []

    def get_value(self, node):
        value = {}
        for property in self.subproperties:
            data = property.parse(node)
            if data is not None:
                value.update(data)
        return value if value else None


class BaseMicroformatParser(NestingMicroformatProperty):
    """ Base class for a microformat parser """

    DEFINITION = ()

    def __init__(self, root, index=None):
        super(BaseMicroformatParser, self).__init__(
            root, index=index,
            subproperties=self.get_subproperties(self.get_definition()))

    def get_subproperties(self, definition):
        retval = []
        for i in definition:
            if isinstance(i, basestring):
                retval.append(BaseMicroformatProperty(i))
            else:
                for k, v in i.iteritems():
                    retval.append(NestingMicroformatProperty(
                        k,
                        subproperties=self.get_subproperties(v)))
        return retval

    def get_definition(self):
        return self.DEFINITION


class MultipleMicroformatParser(NestingMicroformatProperty):
    """ Base class for a parser of multiple microformat properties """

    def __init__(self, root, index=0, subindex=0, parsers=None):
        super(MultipleMicroformatParser, self).__init__(
            root, index=index)
        for parser_class in parsers:
            parser = parser_class(root, index=subindex)
            self.subproperties.extend(parser.subproperties)


class HCardParser(BaseMicroformatParser):
    """ Implementation of an hCard microformat parser """

    DEFINITION = (
        'fn',
        {'n': ('family-name', 'given-name', 'additional-name',
               'honorific-prefix', 'honorific-suffix')},
        {'adr': ('post-office-box', 'extended-address',
                 'street-address', 'locality', 'region',
                 'postal-code', 'country-name', 'type', 'value')},
        'agent',
        'bday',
        'category',
        'class',
        {'email': ('type', 'value')},
        {'geo': ('latitude', 'longitude')},
        'key',
        'label',
        'logo',
        'mailer',
        'nickname',
        'note',
        {'org': ('organization-name', 'organization-unit')},
        'photo',
        'rev',
        'role',
        'sort-string',
        'sound',
        {'tel': ('type', 'value')},
        'title',
        'tz',
        'uid',
        'url'
    )

    def __init__(self, root='vcard', index=None):
        super(HCardParser, self).__init__(root, index=index)


class HCalendarParser(BaseMicroformatParser):
    """ Implementation of an hCalendar microformat parser """

    DEFINITION = ('category', 'class', 'description',
                  'dtend', 'dtstart', 'duration', 'location', 'status',
                  'summary', 'uid', 'url', 'last-modified', 'rdate',
                  'rrule', 'attendee', 'contact', 'organiser',
                  {'geo': ('latitude', 'longitude')}
                  )

    def __init__(self, root='vevent', index=None):
        super(HCalendarParser, self).__init__(root, index=index)


class HResumeParser(BaseMicroformatParser):
    """ Implementation of an hResume microformat parser """

    DEFINITION = ('summary', 'publications')

    def __init__(self, root='hresume', index=None):
        super(HResumeParser, self).__init__(root, index=index)
        self.subproperties.append(HCardParser('contact', index=0))
        self.subproperties.append(HCalendarParser('education'))
        self.subproperties.append(MultipleMicroformatParser(
            'experience',
            index=None, subindex=0, parsers=
            [HCardParser, HCalendarParser]))
        self.subproperties.append(RelTagParser('skill'))
        self.subproperties.append(HCardParser('affiliation'))


class RelTagProperty(BaseMicroformatProperty):
    """ Base class for a rel="tag" microformat property """

    def __init__(self, root='tag', index=0):
        super(RelTagProperty, self).__init__(root, index=index)

    def get_children(self, node):
        return node.find_rel_links(self.root)

    def get_value(self, node):
        href = node.attrib.get('href')
        value = urlparse.urlsplit(href)[2].split('/')[-1] if href else None
        return force_unicode(urllib.unquote_plus(value))


class RelTagHrefUrlProperty(RelTagProperty):

    def get_key(self):
        return 'url'

    def get_value(self, node):
        return force_unicode(node.attrib.get('href'))


class RelTagTextContentProperty(RelTagProperty):

    def get_key(self):
        return 'text'

    def get_value(self, node):
        return self.transform_value(node.text_content())


class RelTagParser(BaseMicroformatParser):
    """ Implementation of a rel="tag" microformat parser """

    def __init__(self, root='tag', index=None, rel='tag'):
        super(RelTagParser, self).__init__(root, index=index)
        self.rel = rel
        self.subproperties = [RelTagProperty(rel),
                              RelTagHrefUrlProperty(rel),
                              RelTagTextContentProperty(rel)]

    def get_children(self, node):
        return node.find_rel_links(self.rel)


### Tools

def cleanup_html(html):
    """Cleanups malformed and wrongly-encoded HTML.
    Returns UTF-8 encoded well-formed HTML"""
    h = html5lib.parse(html, treebuilder='lxml', namespaceHTMLElements=False)
    stream = StringIO()
    h.write(stream, encoding='utf-8')
    return stream.getvalue()


def force_unicode(text, encoding='utf8'):
    """Force ``text`` to be decoded using
    ``encoding``, if not already decoded."""
    if not isinstance(text, unicode):
        return text.encode(encoding)
    return text


def whitespace_cleanup(text):
    """Replace continuous whitespace by a single space"""
    return _re_whitespace.sub(u' ', text).strip()
_re_whitespace = re.compile(r'\s+', re.UNICODE)


# More microformats:
# hReview: http://microformats.org/wiki/hreview
# hAtom: http://microformats.org/wiki/hatom
# rel="license": http://microformats.org/wiki/rel-license
# rel="bookmark": http://microformats.org/wiki/rel-bookmark
# XFN: http://www.gmpg.org/xfn/intro

def linked_parse(url="http://www.linkedin.com/in/dleen/"):
    """ Main program: Parses an hResume from given URL """
    parser = HResumeParser()
    html = urllib2.urlopen(url).read()
    root = lxml.html.fromstring(cleanup_html(html))
    data = parser.parse(root)
    # pprint.pprint(data)
    return data

    #w = csv.writer(open("output.csv", "w"))
    #for key, val in data.items():
    #    w.writerow([key, val])

# if __name__ == '__main__':
#     main(*sys.argv)
