import random, string
import time

def randomWord(length = 6):
   letters = string.ascii_lowercase

   return ''.join(random.choice(letters) for i in range(length))

def prependTimeAndSlug(name=None):
   if name is None:
      raise Exception('A base name is required to prepend timestamp and slug')

   randomSlug = randomWord()
   timestamp = int(time.time())
   nameSections = [timestamp, randomSlug, name]

   return '-'.join(str(x) for x in nameSections)