# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Yaacoub Yaacoub
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        phrase_list = self.phrase.split(" ")
        new_text = ""
        for char in text.lower():
            if char in string.punctuation:
                new_text = new_text + " "
            elif char not in string.punctuation:
                new_text = new_text + char

        new_text_list = new_text.split(" ")
        while "" in new_text_list:
            new_text_list.remove("")

        compare = []
        counter = []
        for word in new_text_list:
            if word in phrase_list:
                compare.append(word)
                counter.append(new_text_list.index(word))

        if len(compare) != len(phrase_list):
            return False
        else:
            for i in range(len(counter) - 1):
                if counter[i + 1] - counter[i] != 1:
                    return False

                for i in range(len(compare)):
                    if compare[i] != phrase_list[i]:
                        return False
            return True


# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):
    def __init__(self, Time):
        self.the_time = (pytz.timezone("EST")).localize(datetime.strptime(Time, "%d %b %Y %H:%M:%S"))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, Time):
        TimeTrigger.__init__(self, Time)

    def evaluate(self, story):
        t = story.get_pubdate()
        if t.tzinfo == None:
            t = (pytz.timezone("EST")).localize(t)
        if t < self.the_time:
            return True
        else:
            return False


class AfterTrigger(TimeTrigger):
    def __init__(self, Time):
        TimeTrigger.__init__(self, Time)

    def evaluate(self, story):
        t = story.get_pubdate()
        if t.tzinfo == None:
            t = (pytz.timezone("EST")).localize(t)
        if t > self.the_time:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1= trigger1
        self.trigger2= trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                filtered_stories.append(story)
    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    list_of_trigger = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggers = {"TITLE": TitleTrigger, "DESCRIPTION": DescriptionTrigger,
                "BEFORE": BeforeTrigger, "AFTER": AfterTrigger,
                "NOT": NotTrigger, "AND": AndTrigger, "OR": OrTrigger}
    used_triggers = {}

    for line in lines:
        L = line.split(",")
        if L[0] != "ADD":
            if len(L) == 3:
                used_triggers[L[0]] = triggers[L[1]](L[2])
            elif len(L) > 3:
                used_triggers[L[0]] = triggers[L[1]](used_triggers[L[2]], used_triggers[L[3]])
        elif L[0] == "ADD":
            for i in range(1, len(L)):
                list_of_trigger.append(used_triggers[L[i]])

    #for line in lines:
    #    L=line.split(",")
    #    if L[0] != "ADD":
    #        if L[1]=="TITLE":
    #            used_triggers[L[0]] = TitleTrigger(L[2])
    #        elif L[1]=="DESCRIPTION":
    #            used_triggers[L[0]] = DescriptionTrigger(L[2])
    #        elif L[1]=="BEFORE":
    #            used_triggers[L[0]] = BeforeTrigger(L[2])
    #        elif L[1]=="AFTER":
    #            used_triggers[L[0]] = AfterTrigger(L[2])
    #        elif L[1]=="AND":
    #            used_triggers[L[0]] = AndTrigger(used_triggers[L[2]], used_triggers[L[3]])
    #        elif L[1] == "OR":
    #            used_triggers[L[0]] = OrTrigger(used_triggers[L[2]], used_triggers[L[3]])
    #    elif L[0] == "ADD":
    #        for i in range(1,len(L)):
    #            list_of_trigger.append(used_triggers[L[i]])

    return list_of_trigger

SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Trump")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Iran")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
