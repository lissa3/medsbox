from django import template
from django.utils.html import format_html

from src.core.utils.tree_help import get_cached_trees

register = template.Library()


class RecrTreeNode(template.Node):
    """for rendering nested comments"""

    def __init__(self, nodelist, queryset_var):
        self.nodelist = nodelist
        self.queryset_var = queryset_var
        # self.post_var = post_var

    def _render_node(self, context, node):
        """ """
        bits = []
        context.push()
        for child in node.get_children():
            bits.append(self._render_node(context, child))
        context["node"] = node
        context["children"] = format_html("".join(bits))

        output = self.nodelist.render(context)
        context.pop()
        return output

    def render(self, context):
        # use the Variable class, instantiate it with
        # the name of the variable to be resolved,
        # and then call variable.resolve(context).
        qs = self.queryset_var.resolve(context)
        roots = get_cached_trees(qs)
        bits = [self._render_node(context, node) for node in roots]

        return "".join(bits)


@register.tag
def recursetree(parser, token):
    """
    Iterates over the nodes in the tree, and renders the contained block for each node.
    This tag will recursively render children into the template variable {{ children }}.
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(("%s tag requires a queryset") % bits[0])

    queryset_var = template.Variable(bits[1])
    nodelist = parser.parse(("endrecursetree",))
    parser.delete_first_token()
    return RecrTreeNode(nodelist, queryset_var)


@register.inclusion_tag("components/comms/comments.html")
def show_comms(post, comments, user, **kwargs):
    return {"comments": comments, "post": post, "user": user, **kwargs}
