from cleo import Command


class AboutCommand(Command):

    name = "about"

    description = "Shows information about mktimeline."

    def handle(self):
        self.line(
            """<info>MKTimeline - timeline creator, static site generator for timelines</info>
<comment>MKTimeline is a static site generator for creating timelines. 
See <fg=blue>https://github.com/jduprey/mktimeline</> for more information.</comment>"""
        )
