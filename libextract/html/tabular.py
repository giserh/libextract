from heapq import nlargest
from libextract.coretools import Counter
from libextract.html import parse_html


SELECT_ALL = '//*'


#TODO: Consolidate get_pairs functions
#TODO: Converge on get_*, filter_*
#TODO: Better yet, decide on "meta/pipelining language"


def children_counter(node):
    """
    Returns the a collections.Counter object measuring the
    frequenies of the children nodes (by tag name) contained
    within a given *node*.
    """
    return Counter([child.tag for child in node])


def get_node_counter_pairs(etree):
    """
    Given an *etree*, returns an iterable of parent
    to child node frequencies (collections.Counter) pairs.
    """
    for node in etree.xpath(SELECT_ALL):
        if len(node):
            yield node, children_counter(node)


def node_counter_argmax(pairs, top=1):
    for node, children in pairs:
        yield node, children.most_common(top)


def sort_best_pairs(pairs, limit=5):
    return nlargest(
        limit,
        pairs,
        key=lambda (node, children): sum(k[1] for k in children),
        )


def filter_tags(pairs):
    """
    Given iterable of (HtmlElement, (html-tag-as-string, frequency)),
    "tagify" (clean up) the parent HtmlElement by filtering
    out child html-nodes whose tag names != html-tag-as-string
    """
    for (node, [(tag, _)]) in pairs:
        for child in node.xpath('./*[not(self::'+tag+')]'):
            node.remove(child)
        yield node


#TODO:Pretty print
def tabularize(nodes):
    """pretty print"""
    pass


STRATEGY = (parse_html,
            get_node_counter_pairs,
            node_counter_argmax,
            sort_best_pairs,
            filter_tags)
