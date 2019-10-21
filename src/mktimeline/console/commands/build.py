from cleo import Command
import json
from ...timeline import Project


class BuildCommand(Command):
    """
    Render timeline project to output directory using the specified template.

    build
        {file? : File to write the timeline to.}
        {--stdout : Write to standard output instead of file.}    
    """

    def handle(self):
        output = self.argument("file")
        self.line("""<info>Outputing timeline to {}.</info>""".format(output))

        project = Project()
        render = project.export2html()

        if self.option("stdout"):
            self.line("""<info>Export to stdout</info>""")
            print(render)
        elif not output:
            self.line("""<error>You must specify an output file or --stdout</>""")
            return 1
        else:
            self.line("""<info>Export to {}</>""".format(output))
            with open(output, "w") as outfile:
                outfile.write(render)

