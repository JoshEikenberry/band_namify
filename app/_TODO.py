"""
Functionlity needed:

rethink blacklist/whitelist data model
clean up / find a way to remove the admin creation endpoint after an admin has been created
import existing band names from Brent's list (separate python script)
make the site pretty (big fonts, colors, icons)
clean up the codebase - remove placeholder comments, example code, tutorial bits
allow limited punctuation in band names (prevent others, like hashtags or brackets)


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
