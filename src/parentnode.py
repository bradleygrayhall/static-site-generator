from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        combined_text = ""
        if self.tag is None:
            raise ValueError
        elif self.children is None:
            raise ValueError("children is missing")
        else:
            for word in self.children:
                combined_text += word.to_html()
            return f"<{self.tag}{self.props_to_html()}>{combined_text}</{self.tag}>"
    