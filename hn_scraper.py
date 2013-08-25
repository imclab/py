
import requests
from BeautifulSoup import BeautifulSoup

# make a single request to the homepage
r = requests.get("https://news.ycombinator.com/")

# convert the plaintext HTML markup into a DOM-like structure that we can search
soup = BeautifulSoup(r.text)

# parse through the outer and inner tables, then find the rows
outer_table = soup.find("table")
inner_table = outer_table.findAll("table")[1]
rows = inner_table.findAll("tr")

stories = []  # create an empty list for holding stories
rows_per_story = 3  # helps us iterate over the table

for row_num in range(0, len(rows)-rows_per_story, rows_per_story):
  
  # grab the 1st & 2nd rows and create an array of their cells
  story_pieces = rows[row_num].findAll("td")
  meta_pieces = rows[row_num + 1].findAll("td")
  
  # create our story dict
  story = {
    "current_position": story_pieces[0].string,
    "link": story_pieces[2].find("a")["href"],
    "title":  story_pieces[2].find("a").string,
  }

  try:
    story["posted_by"] = meta_pieces[1].findAll("a")[0].string
  except IndexError:
    continue  # this is a job posting, not a story

  stories.append(story)

import json
print json.dumps(stories, indent=1)