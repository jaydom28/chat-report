# Chat report
This project reads in a list of messages and provides statistics such as most used words and keyword counts.

## Installation
To clone this repository, use:
> git clone https://github.com/jaydom28/chat-report.git

Install the required libraries with:
> pip3 -r requirements.txt

## Running the script
To run the script, use:

`python main.py [FILES CONTAINING FACEBOOK MESSAGE JSON FILES]`

## To-do
- [x] Read in messages
    - [x] Read in a JSON file of facebook messages
    - [ ] Figure out other ways to get message data
- [x] Analyze each person's messages
    - [x] Filter out odd characters
        - [ ] Find a way to fix the punctuation codes
    - [x] Create a dict of each person's word count (if they are real words)
- [ ] Create visual figures in the following order
    - [ ] Pie Chart of each person's message contribution to conversation (relative to total messages typed in chat)
    - [ ] Pie Chart of each person's word contribution to conversation (relative to total words typed in chat)
    - [ ] Pie Chart of each person's character contribution to conversation (relative to total words typed in chat)
    - [ ] Create figures for each specific word category (MAKE SURE THAT REACTIONS IS A CATEGORY)
        - [ ] Create figures for each individual person
            - [ ] Pie chart showing distribution of each of their words in the category
            - [ ] Show montage of messages that the person typed using the words in the category
        - [ ] Rank each person by ratio (from total words)
        - [ ] Show frequency of words in the category of the course of a year
        - [ ] Train a Markov model to write a page of text using the collective messages of the group that contain the keywords
