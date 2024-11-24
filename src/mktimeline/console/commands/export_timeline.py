import json

from cleo.commands.command import Command
from cleo.helpers import argument, option

from ...timeline import Project


class ExportTimelineCommand(Command):
    name = "export-timeline"
    description = "Export timeline project to Knightlab timeline JSON file format - https://timeline.knightlab.com."
    arguments = [
        argument(
            "jsonfile",
            description="JSON file to write to.",
            default=None,
            optional=True,
        )
    ]
    options = [
        option(
            "--stdout",
            "o",
            description="Write to standard output instead of file.",
            flag=True,
        )
    ]

    def handle(self):
        jsonfile = self.argument("jsonfile")

        project = Project()
        timeline = project.export()

        if self.option("stdout"):
            self.line("""<info>Export to stdout</info>""")
            print(json.dumps(timeline, indent=4))
        elif not jsonfile:
            self.line("""<error>you must specify an output file or --stdout</>""")
            return 1
        else:
            self.line("""<info>Export to {}</>""".format(jsonfile))
            with open(jsonfile, "w") as outfile:
                json.dump(timeline, outfile, indent=4)
