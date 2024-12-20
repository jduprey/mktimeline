import json
import os

import frontmatter
import markdown
from bs4 import BeautifulSoup

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class Event:
    mdfile = ""

    def __init__(self, mdfile):
        self.mdfile = mdfile
        self.event_data = {}
        if os.path.exists(self.mdfile):
            self.event_data = self.to_event()

    def md2json(self):
        """
        Transforms a markdown file with yaml frontmatter to a timeline event in JSON format
        """
        event = self.to_event()

        return json.dumps(event, indent=4)

    def get_inner_html(self, elt):
        if not elt:
            return ""

        return "".join([str(x) for x in elt.contents])

    def build_markdown_content(self):
        """
        Builds the markdown content from the event data
        """
        if "content" not in self.event_data:
            if "text" in self.event_data:
                self.event_data["content"] = f"""# {self.event_data["text"]["headline"]}
{self.event_data["text"]["text"]}"""

    def write_markdown(self):
        """
        Writes a timeline event to a markdown file
        """
        metadata = {key: value for key, value in self.event_data.items() if key != "text" and key != "content"}
        post = frontmatter.Post(self.event_data["content"], **metadata)
        with open(self.mdfile, "w") as f:
            f.write(frontmatter.dumps(post))

    def to_event(self):
        with open(self.mdfile, encoding="utf-8-sig") as f:
            metadata, content = frontmatter.parse(f.read())
        if len(content) == 0 or len(metadata.keys()) == 0:
            raise Exception("Error reading {} or incorrect format.".format(self.mdfile))

        soup = BeautifulSoup(markdown.markdown(content), "html.parser")

        first_element = soup.find()
        try:
            if first_element.name != "h1":
                raise Exception('Expected first element to be an "H1" instead it was {}'.format(first_element.name))
        except Exception as e:
            raise Exception(
                "Failed to parse heading from first element: {}".format(first_element),
                e,
            )

        first_element.extract()
        event = metadata
        caption_elt = BeautifulSoup(markdown.markdown(event["media"]["caption"]), "html.parser")
        credit_elt = BeautifulSoup(markdown.markdown(event["media"]["credit"]), "html.parser")
        event["media"]["caption"] = self.get_inner_html(caption_elt.p)
        event["media"]["credit"] = self.get_inner_html(credit_elt.p)
        event["text"] = {"headline": first_element.text, "text": str(soup)}
        event["content"] = content
        return event
