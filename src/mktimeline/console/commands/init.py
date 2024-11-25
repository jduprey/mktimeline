import os

from cleo.commands.command import Command
from cleo.helpers import argument, option


class InitCommand(Command):
    """
    Initiatlize an MKTimeline project.
    """

    name = "init"
    description = "Initiatlize an MKTimeline project."
    arguments = [argument("dir", description="Initialize dir as an MKTimeline project.", optional=True)]
    options = [
        option(
            "template",
            "t",
            description="The template to use for rending timeline during build.",
            default="template.html",
            flag=False,
        )
    ]

    def handle(self):
        dir = os.getcwd()
        if self.argument("dir"):
            dir = self.argument("dir")
        if not self.confirm("""Create a timeline project in directory "{}"?""".format(dir), False):
            return
        self.line("""<info>Initializing MKTimeline project in directory "{}".</info>""".format(dir))

        from mktimeline.timeline import Project

        Project.init(dir, self.option("template"))
