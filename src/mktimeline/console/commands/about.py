from cleo.commands.command import Command

from mktimeline import __version__


class AboutCommand(Command):

    name = "about"

    description = "Shows information about mktimeline."

    def handle(self):
        self.line(
            f"""<info>MKTimeline {__version__} - timeline creator, static site generator for timelines</info>
<comment>MKTimeline is a static site generator for creating timelines. 
See <fg=blue>https://github.com/jduprey/mktimeline</> for more information.</comment>"""
        )
