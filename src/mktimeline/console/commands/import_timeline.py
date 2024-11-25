import json

from cleo.commands.command import Command
from cleo.helpers import argument

from mktimeline.timeline.project import Project


class ImportTimelineCommand(Command):
    name = "import-timeline"
    description = "NOT IMPLEMENTED YET - Import timeline from Knightlab timeline JSON file format - https://timeline.knightlab.com/."

    arguments = [
        argument(
            "jsonfile",
            description="JSON file that follows Knightlab timeline JSON file format - https://timeline.knightlab.com/",
        )
    ]

    def handle(self):
        jsonfile = self.argument("jsonfile")
        self.line("""<info>Import from {}</info>""".format(jsonfile))

        with open(jsonfile) as r:
            timeline = json.load(r)

        project = Project()
        project.import_data(timeline)

        self.line(f"<info>Timeline imported with {len(project.timeline['events'])}" " events</info>")
