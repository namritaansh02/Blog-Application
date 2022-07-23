## Introduction

I learnt django via corey schafer tutorials and on the way generated a very basic blogging application following the tutorial. Later on tried to emulate reddit by features such as credits for a user, upvoting or downvoting blogs. Added commenting feature over each blog with upvoting or downvoting blogs. I am now planning to add a search bar over the website to search for user or blog. After I would add a basic messaging feature between user however it would have no end to end encrypting which should be there. So it would be the next step. I used bootstrap for frontend. 

## Database Setup on Postgres

User:
1. User ID : Primary Key
2. Username
3. Email
4. Profile Photo

Comment:
1. Comment ID : Primary Key
2. Post ID : Foreign Key
3. User ID : Foreign Key
4. Votes
5. Content

Blog:
1. Blog ID : Primary Key
2. User ID : Foreign Key
3. Date Field
4. Content
5. Votes

Blog Vote:
1. BlogVote ID : Primary Key
2. Blog ID : Foreign Key 
3. Value

Comment Vote:
1. CommentVote ID : Primary Key
2. Comment ID : Foreign Key
3. Value

## Django Tutorials

https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
