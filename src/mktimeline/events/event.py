import json

import markdown
from bs4 import BeautifulSoup
from frontmatter import Frontmatter

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class Event:
    mdfile = ""

    def __init__(self, mdfile):
        self.mdfile = mdfile

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

    def to_event(self):
        with open(self.mdfile, encoding="utf-8-sig") as f:
            post = Frontmatter.read(f.read())
        if len(post["body"]) == 0 or len(post["frontmatter"]) == 0:
            raise Exception("Error reading {} or incorrect format.".format(self.mdfile))

        soup = BeautifulSoup(markdown.markdown(post["body"]), "html.parser")

        first_element = soup.find()
        try:
            if first_element.name != "h1":
                raise Exception(
                    'Expected first element to be an "H1" instead it was {}'.format(
                        first_element.name
                    )
                )
        except Exception as e:
            raise Exception(
                "Failed to parse heading from first element: {}".format(first_element),
                e,
            )

        first_element.extract()
        event = post["attributes"]
        caption_elt = BeautifulSoup(
            markdown.markdown(event["media"]["caption"]), "html.parser"
        )
        credit_elt = BeautifulSoup(
            markdown.markdown(event["media"]["credit"]), "html.parser"
        )
        event["media"]["caption"] = self.get_inner_html(caption_elt.p)
        event["media"]["credit"] = self.get_inner_html(credit_elt.p)
        event["text"] = {"headline": first_element.text, "text": str(soup)}
        return event
