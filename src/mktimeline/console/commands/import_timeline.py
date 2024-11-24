from cleo.commands.command import Command

from mktimeline.timeline.project import Project


class ImportTimelineCommand(Command):
    """
    Import timline from Knightlab timeline JSON file format - https://timeline.knightlab.com/.

    import
        {jsonfile : JSON file that follows Knightlab timeline JSON file format - https://timeline.knightlab.com/}
    """

    name = "import-timeline"

    def handle(self):
        jsonfile = self.argument("jsonfile")
        self.line("""<info>Import from {}</info>""".format(jsonfile))

        with open(jsonfile) as r:
            timeline = json.load(r)

        project = Project()
        project.import_(timeline)
