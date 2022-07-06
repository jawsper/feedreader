class DisplayTitleMixIn:
    @property
    def display_title(self):
        return self.title if self.title else "(no title)"
