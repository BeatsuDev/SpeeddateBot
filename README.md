# Speed date Discord Bot

This is a Discord bot that facilitates speed dates in Discord. It can be used in many contexts; speed *dates*, talking about feelings, getting to know more people in a community etc. The goal is in the end just to make it easier for people to open up. This bot is made for Oslo Katedralskole's Discord as of now and won't be public soon.

> "*It's like a rotating roulette of people where you can open up to people and meet new people*"

Usage
----

The bot runs primarily through commands. Available commands are:

`help` - Shows a help message

`start` - Starts the rotation in VoiceChannels and connected Text Channels or continues the ongoing one

`pause` - Pauses the rotation

`stop <keep>` - Stops the rotation; deletes the voice channels and text channels after a set amount of time, unless the parameter "keep" is given.

### Example:

    !start
    *rotation starts*

    !pause
    *rotation is paused, users stay where they are*

    !start
    *rotation continues*

    !stop keep
    *rotation stops, users are disconnected and the Voice and Text Channels are kept*


Configuration
----

The bot has some configuration settings that can be changed for each server.

`prefix` - The prefix to invoke commands to the bot

`delay` - The delay after a rotation is stopped and to the Text Channels and Voice Channels being deleted.

Contribution
----
If you want to contribute; fork this repository, **create a new branch** named something related to your change, then submit a pull request explaining the changes you made in this format:


    Problem fix/Implementation:
    How you fixed it/How it works:
    What parts of the bot does this affect:

Make sure to follow PEP8 standards.
