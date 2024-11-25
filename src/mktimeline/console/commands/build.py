
from cleo.commands.command import Command
from cleo.helpers import argument, option

from ...timeline import Project


class BuildCommand(Command):
    name = "build"
    description = (
        "Render timeline project to output directory using the specified template."
    )
    arguments = [
        argument(
            "file",
            description="File to write the timeline to.",
            optional=True,
            default=None,
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
