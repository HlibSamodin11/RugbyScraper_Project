from database import (
    insert_team,
    insert_competition,
    insert_standing,
    insert_match,
    log_scrape,
    initialise_database,
)
from datetime import datetime

# make sure tables exist
initialise_database()

# test inserting a team
insert_team("Ireland", "IRE", "Ireland", "Six Nations")
insert_team("England", "ENG", "England", "Six Nations")
print("teams inserted")

# test inserting a competition
insert_competition("Six Nations 2026", "international", "2026")
print("competition inserted")

# test inserting a standing
insert_standing(1, 1, 1, 4, 4, 0, 0, 18, datetime.now().strftime("%Y-%m-%d"))
print("standing inserted")

# test inserting a match
insert_match(1, "Ireland", "England", 24, 18, "2026-02-15")
print("match inserted")

# test logging a scrape
log_scrape(5, "success")
print("scrape logged")

print("all tests passed!")
