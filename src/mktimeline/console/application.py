from .commands import AboutCommand
from .commands import ImportTimelineCommand
from .commands import ExportTimelineCommand
from .commands import BuildCommand
from .commands import InitCommand
from cleo import Application


def main():
    application = Application()
    application.add(AboutCommand())
    application.add(ImportTimelineCommand())
    application.add(ExportTimelineCommand())
    application.add(BuildCommand())
    application.add(InitCommand())
    application.run()


if __name__ == "__main__":
    main()
