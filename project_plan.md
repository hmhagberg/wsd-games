# WSD Project Plan
Henri Hagberg 294858
Tommi Oinonen 292070
Patrick Patoila 295970

## Features
Were planning to do all extra features (our goal is +3). To be honest, we aren't completely sure how easy these features are to do but they seem (for the most of the part) rather easy.

* Save/load feature
    - Since we are already going to implement some messages as part of mandatory requirements it makes sense to implement them all
* 3rd party login
    - We'll investigate implementing Gmail and/or Facebook login (they both use same technology, OAuth)
* RESTful API
    - Implementing API will be straightforward: (for public information such as game lists and high scores) simply render database query results as JSON
    - Private information (developer stats, for example) need authorization though
* Own game
    - We're planning to do a simple snake game with multiple levels
* Mobile friendly
    - We're going to use Bootstrap so responsive desing requires little to no extra effort
* Social media sharing
    - Sharing can be implemented with a simple plugin

## Roadmap
### Mandatory features
* Users
    - Register
    - Buy games
        * Payment system
    - Play games
    - Search and browse games
* Developers
    - Register
    - Create games
    - Manage games
    - Game statistics
* Game/service interaction
    - Get high score from game
* Authentication
    - Login, logout, register
    - Email validations

### What we actually need to do
* DB tables for everything
    - Users
    - Developers
    - Games
    - The ER diagram in repository root shows basic database structure (mainly relations, no attributes and so on)
* Views
    - General
        * Front page
        * Login view
        * Registration views
    - Game views
        * Store view
        * Play view
        * Developer view (for managing)
    - User
        * Profile view
    - Dev
        * Profile view
        * Dashboard
    - Browsing views
        * By category
        * By developer
    - API views
        * Public and authenticated

### Schedule
1. View stubs (i.e. dump content without any styling)
2. Basic database structure
    - Email authentication stub
3. When things seem to work start polishing UI
    - Start implementing responsive design at this point
4. Integrating games and payment system
5. Test deploying to Heroku
6. After mandatory features are working start implementing extra features
    - Extra features don't seem to depend on each other so their implementation order doesn't
    - However we probably start from API, 3rd party login and save/load
7. Write final document and deploy

Also, because there are three of us we can do several things at the same time (for example, do view stubs and database at the same time). About actual scheduling: we start actually working on the project in early January (by 7th at latest). That leaves us about 5 weeks to work. We'll probably try to do ~weekly milestones and get mandatory features done in 3 weeks. 


## Tools
The main project tool we're planning to use is Gitlab. We use issues to keep track of tasks and who will be doing them. Milestones help us track overall progress. Wiki is useful for documentation, for example. We create a single repository where the master always contains a working product. Then when developing features we create a new branch for each feature and merge them to master when they are working.

For communication we use IM. About face-to-face meetings we don't have any plans but we probably meet quite often (at least once a week). Peer programming has proved out to be quite useful in past. 

We also consider using some test framework. Automated tests (if we get them work) will make our life easier when developing. Testing is also a subject we would like to learn more about.

Toggl will be used to track time spent on various tasks.