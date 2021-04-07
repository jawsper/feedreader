from django.core.management.base import BaseCommand
import os
import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from feedreader.models import Outline, Feed


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("[Outline importer]")
        if len(args) != 2:
            self.stdout.write("Please supply the user id and the filename to import.")
            return
        try:
            self.user = User.objects.get(pk=int(args[0]))
        except User.DoesNotExist:
            self.stdout.write("User does not exist!")
            return
        filename = args[1]
        if not os.path.exists(filename):
            self.stdout.write("File does not exist!")
            return

        self.outlines = 0
        self.feeds = 0

        data = ET.parse(filename)
        root = data.getroot()
        body = root.find("body")
        for outline in body:
            if "type" in outline.attrib:
                self.import_outline_feed(outline.attrib)
            else:
                parent = self.import_outline(outline.attrib)
                for child in outline.findall("outline"):
                    self.import_outline_feed(child.attrib, parent)
        self.stdout.write("Completed!")
        self.stdout.write(
            "Added {0} new outlines and {1} new feeds".format(self.outlines, self.feeds)
        )
        return

    def import_outline(self, data):
        outline = Outline(user=self.user, title=data["title"])
        outline.save()
        self.outlines += 1
        return outline

    def import_outline_feed(self, data, parent=None):
        try:
            feed = Feed.objects.get(xml_url=data["xmlUrl"])
        except Feed.DoesNotExist:
            feed = Feed(
                title=data["title"], xml_url=data["xmlUrl"], html_url=data["htmlUrl"]
            )
            feed.save()
            self.feeds += 1
        try:
            outline = Outline.objects.get(feed=feed, user=self.user)
        except Outline.DoesNotExist:
            outline = Outline(
                user=self.user, parent=parent, title=data["title"], feed=feed
            )
            outline.save()
            self.outlines += 1
