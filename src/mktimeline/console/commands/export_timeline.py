import json
from cleo import Command
from ...timeline import Project


class ExportTimelineCommand(Command):
    """
    Export timline project to Knightlab timeline JSON file format - https://timeline.knightlab.com/.

    export
        {jsonfile? : JSON file to write to.}
        {--stdout : Write to standard output instead of file.}    
    """

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
                print(json.dump(timeline, outfile, indent=4))

