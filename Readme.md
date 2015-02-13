# Project document

Henri Hagberg 294858
Patrik Patoila 295970
Tommi Oinonen 292070

## The service

The service is running at http://wsd-games.herokuapp.com. The service has been initialized with few developers, games and players. One game (Worm Game) was developed by us and all the other games serve the provided example game.

For testing things use these credentials:

Type        Username    Password
Player      pekkis      test
Developer   pelifirma   test


## Mandatory features

### Authentication
Login, logout and signup are all implemented for both players and developers. All of these are based on Django’s built-in implementations. Emails are validated and for “sending” activation emails we use Django’s console backend.

Security restrictions are in place: players can play only owned games and developers can manage only their own games. Player and developer functions are separated. For example, players can’t add games.

Restrictions are based on data in database. For example, if user accesses a game page, the service checks if there is an ownership associated with the authenticated user and the game. If there is, the user is allowed the play the game. Likewise, if the user is a developer and she is marked as the game’s developer she can manage it.

Multiple users can log in on same account at the same time. Ideally this would be prevented but at least the service doesn’t crash.

**Points: 195/200**
Email validation is implemented and system is robust and done cleanly


### Basic player functionalities
Players are able to buy games using the payment service and can play them after they are bought. Games can be browsed by category and by developer. There is also a search function and games can be sorted by name, price or developer. The search function searches all data inside the cards. The cards, which don’t have anything to match the search query, are hidden and only the matched cards are visible to the user. The search is not case sensitive.

Users (both players and developers) have profiles and ability to edit them. The profiles are very basic however: you can’t choose what fields to hide or show and currently pretty much everything is hidden in players’ profiles. Player profiles aren’t very discoverable either. The whole feature, however, isn’t listed in requirements and should be considered as extra.

**Points: 280/300**
All mandatory (and some extra) features are implemented and work well. Profile implementation is a bit weak.


### Basic developer functionalities
Developers can add games and manage (edit details, remove) them. Removing a game simply deletes the game object and its references in the database. Removing works without errors but players who have bought the game don’t receive any notification etc. This should be improved (e.g. set some flag in DB instead of actually deleting game).

Developers can view statistics about the games they have published (open game card -> “Inspect”). The statistics include game sales over various time periods. There is no aggregate data or data about number of times games are played.

**Points: 190/200**
Required features implemented. Game removing is not very elegant.


### Game/service interaction
Highscores are stored and displayed on game page. Whenever user submits a new highscore it is saved to DB and loaded to page through our service’s API using Ajax. Messages are implemented as well (though they aren’t used much).

**Points: 200/200**
Highscores are stored and top 10 is displayed on game page. Scores on page are updated almost in real-time.


### Quality of work
The interface of our service is consistent and while not overly flashy it is relatively stylish. We’ve tried to embrace DRY principle and extract functionality into clearly defined blocks. This can be seen especially well with forms (both in views and in templates). There’s probably still quite a few things that could be done with less repetition: as the project went on we discovered that Django offers dozens of base classes for various situations.

Boundary between business logic and presentation is also clear. Payment and API system could have been implemented as separate apps.

Our code style and conventions aren’t very consistent. Each of us has different preferences for doing things and we never really decided what style we should use. Despite inconsistencies the code itself should be still quite clear and understandable. There’s some JavaScript mixed with templates. This is because we needed template variables in the code. There probably would have been some way around this, however.

The documentation was left a little thin because in general we were all quite involved in the work of others that it wasn’t necessary to comment heavily during the development. Therefore the code is not very extensively commented.

Overall we haven’t discovered any major weaknesses in our service or its implementation.

**Points: 90/100**


## Extra features

### Save/load feature
Feature works and it is implemented using the message protocol. The saved data is fetched from the database when the game page is loaded and they are sent to the game when the game requests them. This means that that if new data is saved to the database, the new data can’t be fetched without refreshing the page. We removed this problem in our game by saving the data also locally to the game where it can be used in the same session.

In our own game load_request message is sent once when the user loads the game page. If the game receives load message with saved data, there will be “continue game” in the main menu of the game. If the database doesn’t have the saved data, the service will send a message to the game that informs the game that there is no saved data. When there is no saved data in the database the “continue game” option will be hidden and disabled.

The save feature can be used when the game is paused. The data is saved to the database and to the game’s Javascript code. If the player chooses to continue the game in the same session, the saved data will be fetched from the Javascript code. If the player continues the game in a different session the saved data is fetched from the service’s database.

**Points: 85/100**


### 3rd party login
Google+ can be used for signup/login. The feature is implemented using python-social-auth (https://github.com/omab/python-social-auth). The package supports Django pretty much out of the box. We had to customize the authentication pipeline a bit, however. Firstly, user is asked for username. Secondly, user’s profile is saved (profile is separate from actual account). Thirdly, a login/signup confirmation is displayed.

Only players can utilize Google+ login. We didn’t feel it would be necessary for developers to be able to use G+ login (it probably wouldn’t be very realistic). Also, players’ emails aren’t validated when they signup via Google+. This is intentional since Google already does validation.

**Points: 100/100**


### RESTful API
We implemented RESTful API that can be used to get information (it can’t be used to post anything). It ended pretty modular and would have probably worked as a separate app. V1 API’s URL scheme is as follows:

    /api/v1/<collection>.<format>
    /api/v1/<collection>/<id>.<format>

Basically, the user decides from which collection (of models which could be something else aswell) he/she wants retrieve information. Supported collections are: profiles, games, categories, developers. If he/she wants to retrieve all objects in the collection then he/she doesn’t specify any IDs. Parameters limit and offset can be used to limit the number of objects returned.
Example: /api/v1/categories.json

If the user wants to retrieve specific object she can specify the ID. In our service its always object’s slug. When retrieving a single object user can also supply her API key as query parameter (api_key). If user is identified as the owner of the object then confidential information is also included in the response.
Example: /api/v1/games/angry-birds.json

Currently only JSON is supported as response format

**Points: 100/100**
The API is sensible and requires authentication for confidential data. The implementation is also quite modular.


### Own game
There was an old and very simple javascript worm/snake game that Patrick had made. We improved and modified it to work as a game that our service serves. The game has options that can be chosen with number keys and and the game itself is played using “wasd”. The game uses the highscore system of the service and allows saving the game state which however isn’t very useful in this particular game.

The game is developed using createjs libraries (http://www.createjs.com/Home). We published the game in http://ragoz4.arkku.net/ that we could use it in our services iframe. The entire code of the game is also in git (/worm_game/).

**Points: 100/100**


### Mobile friendly
We disabled playing on mobile devices because the iframe destroyed the layout and at least our own game can’t be played on mobile. Realistically though there probably would be some flag that developers could set if the game was playable on mobile. We used Bootstrap (http://getbootstrap.com/) to make our service responsive and therefore making it mobile friendly. Our service is mostly based on cards. The cards adapt well to different screen sizes. When there are multiple cards in one page we display them in a grid. The grid adapts to the screen sizes. In large screens (usually desktop) the cards are shown in four columns, in little smaller screens (usually tablets) cards are in two columns and in very small screens (usually smartphones) the cards are in a single column.

Our navigation bar is also mobile friendly. When the service is used with a small screened device the options of the navigation bar are hidden under a single button. When the button is pressed, it opens a menu where the user can easily select the option he wants.

**Points: 45/50**


### Social media sharing
Social media sharing is possible for Google+. The share button was basically added to our pages as off-the-self from Google. Since title and image are the only metadata we can add to the post we had to cram both the game name and description to the title. The user can freely add comment to the post, however. Also, only game pages can be shared.

The share button caused some errors when we validated our HTML5 code using an online validator (http://validator.w3.org/). The Google+ share button adds an iframe to our HTML code which has few attributes that cause errors and it contains CSS styling that the validator advises us to move to a CSS file.

**Points: 40/50**


## Teamwork and project in general
We had meetings for the project two times a week. In the meetings we discussed any architectural decisions and agreed on who would implement what next. Apart from the meetings we relied on IM. Most of the code was written separately and a bit more communication could have rendered the code generally more consistent. Due to our own preferences the front end was mainly done by Patrick while Henri and Tommi focused on the back end. The work was quite evenly divided over the past month. We had planned to write tests for the system and Tommi actually did some investigation on the topic. We had also planned that we would track the time spent on the project but eventually we didn’t.
Our main project management tool was Gitlab. We used issues to keep track of who was doing what feature and what features and fixes we still had to do. We also had ~weekly milestones to help with scheduling but we didn’t adhere to these very strictly.


## Usage
Using the service should be quite simple and most functions are self-explanatory. The navigation bar hosts the most important links (to e.g. signup, login, user’s profile).

Clicking game cards offers option buy/inspect games for logged in users. After the game has been bought it can be played by clicking the link on the game card.

For testing purposes there’s some data in a fixture named wsd-games-data.xml.
