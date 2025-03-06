from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("method to_html() not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        return reduce(lambda acc, tup: acc + f' {tup[0]}="{tup[1]}"', self.props.items(), "") 

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value is mandatory")
        if self.tag == None:
            return self.value 

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag is mandatory")
        if not self.children:
            raise ValueError("missing children attribute")
        return f'<{self.tag}{self.props_to_html()}>{reduce(lambda acc, node: acc + node.to_html(), self.children, "")}</{self.tag}>'


