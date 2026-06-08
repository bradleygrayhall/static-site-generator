from __future__ import annotations

class HTMLNode:
    def __init__(self,tag: str|None=None,value: str|None=None,children: list[HTMLNode]|None=None,props:dict[str,str]|None=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_str = ""
        if self.props is not None:
            for prop in self.props:
                html_str += f' {prop}="{self.props[prop]}"'
        return html_str
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"