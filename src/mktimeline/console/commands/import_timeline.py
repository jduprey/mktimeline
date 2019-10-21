from cleo import Command


class ImportTimelineCommand(Command):
    """
    Import timline from Knightlab timeline JSON file format - https://timeline.knightlab.com/.

    import
        {jsonfile : JSON file that follows Knightlab timeline JSON file format - https://timeline.knightlab.com/}    
    """

    def handle(self):
        jsonfile = self.argument("jsonfile")
        self.line("""<info>Import from {}</info>""".format(jsonfile))

