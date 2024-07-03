# libre-mate: an online book club

![Website homepage on different devices](docs/am-i-responsive.png)

Developed by Benedict Amory Chambers
## Table of Contents

1. [Project Goals](#project-goals)
    1. [User Goals](#user-goals)
    2. [Site Goals](#site-goals)
2. [User Experience](#user-experience)
    1. [Target Audience](#target-audience)
    2. [User Stories](#user-stories)
3. [Design](#design)
    1. [Design Choices](#design-choices)
    2. [Colours](#colours)
    3. [Fonts](#fonts)
    4. [Structure](#structure)
    5. [Wireframes](#wireframes)
4. [Technologies](#technologies)
    1. [Languages](#languages)
    2. [Frameworks and Tools](#frameworks-and-tools)
5. [Features](#features)
6. [Testing](#testing)
    1. [HTML Validation](#HTML-validation)
    2. [CSS Validation](#CSS-validation)
    3. [JavaScript Validation](#javascript-validation)
    4. [Accessibility](#accessibility)
    5. [Performance](#performance)
    6. [Compatibility](#compatibility)
    7. [Testing user stories](#testing-user-stories)
7. [Bugs](#bugs)
8. [Credits](#credits)
9. [Deployment](#deployment)
10. [Acknowledgements](#acknowledgements)

## Project Goals 

This is a community-focused online library where users can create their own customised bookshelf with full database CRUD functionality; a user can decide to make their content private, but there is a community tab for sharing books and thoughts with other readers that may encourage them to buy and read something new.

### User Goals 

- A simple, clear, visually appealing way to catalogue and store their library online
- A space to preserve their thoughts about a book and to read others' thoughts
- Full control over their own content and data that has been stored in the database, in terms of privacy and in editability 

### Site Goals

- A clear and easy-to-navigate layout for all information
- An accessible and responsive site that ensures an equally good experience regardless of how the user wants to interact with the site
- Efficient, useful data management and access, providing a valuable resource for users
- Option to monetise the site by use of referral links to buy books from user recommendations

### Developer Goals

- Create a site that allows users to easily and intuitively interact with a database
- Design the site to make valuable and enjoyable use of the data provided by users
- The site is accessible to a wide range of users, with a clear and easy-to-navigate structure for all information
- Customise the experience to appeal to the target demographic and to foster a sense of community

## User Experience

### Target Audience

- Readers and book enthusiasts
- Bloggers and reviewers
- Authors who may be interested in having their books reviewed on the site

### User Stories

## Design 

### Design Choices

I have opted for as simple and uncluttered a design as possible, drawing the attention more solely to the books on display. I have used a translucent overlay for all site content, on top of a background image that conveys the theme and tone of the site's design. By keeping the content within a relaxed, flat colour background, I intended to make both the content and the way that users can interact with the content clearer and more intuitive.

### Colours

I used [HTML Color Codes](https://htmlcolorcodes.com/color-picker/) to choose two analogous complementary colours for both the primary background and accent colours.

![Colour Scheme](docs/colour.png)

### Fonts

I used two fonts on the website; one of which I used for the main brand image and link present in the header of every page, which is a display font conveying tone, and one clearer font for any body of text in the site, which is easier and clearer to read.

[Whisper](https://fonts.google.com/specimen/Whisper) - Display font

[Cactus Classical Serif](https://fonts.google.com/specimen/Cactus+Classical+Serif) - Main text font

### Structure

The site consists of eight main pages with several supplementary pages for clear functionality.

1. My Library - This is the homepage for logged in users. It displays the user's books, which can be sorted by several different datapoints, and allows the user to add new books or genre tags to their library. This page links to two supplementary pages, with forms to submit new books and genre names to the database.

2. View Book - Each book in the user's library can be viewed individually for visual clarity and to see further information. This page links to one supplementary page, which is a form the user can submit to edit the data associated with this book in the database.

3. Community - This page focuses on the community building aspect of the site. It displays the most recent entries and reviews created by users, as long as the user has a public account. This is where users can see what other people are reading, and read the thoughts they have posted on the book, potentially leading to referral link sales.

4. Register - A form for the creation of a new user in the database, with the option to choose a private or public account. This page links to the Sign In page for users who already have an account.

5. Sign In - A form that allows users to log in to their account. This page links to the Register page for users that do not yet have their own account.

6. Account - This page allows users to manage their account. Here, they can edit or delete their own custom genre tags, can switch between a public and private account, and can delete their account and all related data entirely if they wish.

7. About - A short page explaining the site's ethos and goals to the user.

8. 404 - A custom 404 page redirecting the user to either their own library or to the Sign In page when navigating to an unknown URL.


## Technologies

### Languages 

HTML5

CSS3

JavaScript

Python

Jinja2

### Frameworks and Tools

[Flask](https://flask.palletsprojects.com/en/3.0.x/)

I built this web application in Flask, in order to make use of templating and to use Python on the backend for accessing and manipulating the database.

[SQLAlchemy](https://www.sqlalchemy.org/)

I used the SQLAlchemy ORM to write efficient, clean Pythonic code for manipulating the database.

[EDrawMax](https://www.edrawmax.com/online/en/)

I used this tool to develop an Entity Relationship Diagram during the planning stages of my project.

[Open Library Covers API](https://openlibrary.org/dev/docs/api/covers)

This API provides cover images of books from their database, using an ISBN provided by the user. 

[Bootstrap](https://getbootstrap.com/)

[Visual Studio Code](https://code.visualstudio.com/)

[Git](github.com)

[Heroku](heroku.com)

[Google Fonts](https://fonts.google.com/)

[Balsamiq](https://balsamiq.com/)

[Obsidian](https://obsidian.md/)

[Font Awesome](https://fontawesome.com/)

[Favicon](https://favicon.io/)

[W3C Markup Validation Service](https://validator.w3.org/)

[W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)

[JSLint](https://www.jslint.com/)

[CI Python Linter](https://pep8ci.herokuapp.com/)

[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

[WAVE Web Accessibility Evaluation Tools](https://wave.webaim.org/)
