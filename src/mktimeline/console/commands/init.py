import os
from cleo import Command


class InitCommand(Command):
    """
    Initiatlize an MKTimeline project.

    init
        {dir? : initialize dir as an MKTimeline project}
        {--t|template=template.html : template to use for rending timeline during build. }
    """

    def handle(self):
        dir = os.getcwd()
        if self.argument("dir"):
            dir = self.argument("dir")
        if not self.confirm(
            """Create a timeline project in directory "{}"?""".format(dir), False
        ):
            return
        self.line(
            """<info>Initializing MKTimeline project in directory "{}".</info>""".format(
                dir
            )
        )

        from mktimeline.timeline import Project

        Project.init(dir, self.option("template"))

