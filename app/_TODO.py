"""
Phase I Functionlity needed:

figure out how to create an admin account in the db directly for security sake
clean up the codebase - remove placeholder comments, example code, tutorial bits
deploy - figure out how NFS.net works, SSH, deployment scripts, bash scripts, etc
probably need a logo
submit band name page needs some styling work



phase II:
monetization - basic ads
t-shirt addon - e-store that sells band names on t-shirts (random font and images?)
ROBOT MODE: Return a randomly constructed band name (lots of fun here - maybe pull from existing submissions,
 or seed words, random combinations/compound words (ie rand(1-5), which_words_compound, etc). Users can then "vote"
 to add it to the db
import existing band names from Brent's list (separate python script)
fontawesome logos: random 1-3 fontawesome icons displayed underneath each random band name
rethink blacklist/whitelist model - it's kind of clunky in how it works
unit testing




finished tasks:
buttons look ugly on upbote/report
make the site pretty (big fonts, colors, icons) ** done enough for phase I
allow limited punctuation in band names (prevent others, like hashtags or brackets - this is regex)
Capitalize Every Word Submitted **DONE
create single Admin user (separate python script for deployment) ** DONE BUT HACKY
admin pages (reuse flask tutorial's login logic to make admin page) **DONE
hide blacklist/whitelist endpoints behind admin login **DONE
random band name page (rand function pulls single band from db) **DONE
upvote endpoint **DONe
unique band name check **DONE
blacklist endpoint **DONE
whitelist endpoint **DONE
report endpoint **DONE
upvote endpoint **DONE
report button on page **DONE
upvote button on page **DONE
admin blacklist page **DONE
top votes page ** DONE
find a way to hash band ids to make them obfuscated in urls etc. flask obscure ** DONE
rate limiting endpoints to prevent upvote/report abuse ** DONE, flask-limiter
"""
