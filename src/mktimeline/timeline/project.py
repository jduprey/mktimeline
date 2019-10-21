import json
import shutil
import yaml
import os
import re
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

import importlib.resources as pkg_resources

from .. import templates

from ..events import Event

# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
# https://docs.python.org/3.8/library/importlib.html?highlight=importlib#module-importlib.resources
# for i in pkg_resources.contents(templates):
#     print(i)

# template_path = pkg_resources.path(templates, ".")
# print("PATH: {}".format(template_path))

project_fname = "timeline_project.yml"

title_template = """---
media:
  caption: {media[caption]}
  credit: {media[credit]}
  url: {media[url]}
---

# {heading}

{description}
"""


class Project:
    """
    Timeline Project
    """

    project_data = {}
    project_dir = os.getcwd()
    events_dir = os.path.join(project_dir, "events")
    project_file = os.path.join(project_dir, project_fname)
    timeline = {}

    def __init__(self):
        if not os.path.exists(self.project_file):
            raise Exception("Missing project data.")

        with open(self.project_file) as r:
            self.project_data = yaml.load(r)

        self.timeline = self.export()

    @staticmethod
    def init(project_dir, template):
        title_data = {
            "heading": "HEADLINE",
            "description": "DESCRIPTION",
            "media": {"caption": "CAPTION", "credit": "CREDIT", "url": "URL"},
        }

        data = {"template": template, "templates_dir": "templates"}

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        if os.path.exists(os.path.join(project_dir, project_fname)):
            print("Project file already exists.")
        else:
            with open(os.path.join(project_dir, project_fname), "w") as f:
                yaml.dump(data, f, default_flow_style=False)

        events_dir = os.path.join(project_dir, "events")
        if os.path.exists(events_dir):
            print("Project events directory already exists.")
        else:
            os.makedirs(events_dir)

        with open(os.path.join(project_dir, "title.md"), "w") as f:
            f.write(title_template.format(**title_data))

        shutil.copytree(
            templates.__path__[0],
            os.path.join(project_dir, data["templates_dir"]),
            ignore=shutil.ignore_patterns("*.py", "*.pyc", "__py*"),
        )

    def export(self):
        ev = Event("title.md")
        title = ev.to_event()

        events = []
        for filename in Path("events").glob("**/*.md"):
            ev = Event(filename)
            if ev:
                events.append(ev.to_event())

        for ev in events:
            if "month" in ev["start_date"]:
                ev["start_date"]["month"] = ev["start_date"]["month"].rjust(2, "0")
            if "day" in ev["start_date"]:
                ev["start_date"]["month"] = ev["start_date"]["day"].rjust(2, "0")

        # Make sure events are sorted by start date
        events.sort(
            key=lambda event: "{0[year]}-{0[month]}-{0[day]}".format(
                defaultdict(str, **(ev["start_date"]))
            ),
            reverse=False,
        )

        timeline = {"title": title, "events": events}
        return timeline

    def export2html(self):
        # Fix title media
        if self.timeline["title"]["media"]["url"].find("//youtu") != -1:
            self.timeline["title"]["media"]["url"] = re.sub(
                r".*\/(.*)$",
                r"https://youtube.com/embed/\1?rel=0",
                self.timeline["title"]["media"]["url"],
            )

        # Make sure events are sorted by start date
        self.timeline["events"].sort(
            key=lambda event: "{0[year]}-{0[month]}-{0[day]}".format(
                defaultdict(str, **(event["start_date"]))
            ),
            reverse=False,
        )

        # Convert media youtube URLs to embed urls...
        for ev in self.timeline["events"]:
            if (
                "media" in ev
                and "url" in ev["media"]
                and ev["media"]["url"].find("//youtu") != -1
            ):
                ev["media"]["url"] = re.sub(
                    r".*\/(.*)$",
                    r"https://youtube.com/embed/\1?rel=0",
                    ev["media"]["url"],
                )

        env = Environment(
            # loader=PackageLoader("mktimeline", "templates"),
            loader=FileSystemLoader(self.project_data["templates_dir"]),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # Generate the HTML from the template
        template = env.get_template(self.project_data["template"])
        return template.render(self.timeline)
