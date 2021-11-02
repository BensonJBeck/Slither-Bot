# Slither-Bot
A python supreme bot which comes packed with a UI and file management system
Slither bot is meant to be compiled from source as an educational project. Slither bot is incapable of purchasing items but can be modified to do so. Slither bot has been tested and proven to work on drop day. ***No user information is stored securley.*** That being said anyone using slither bot should delete user profiles containing sensitive information after use. 

### How to use ###
1. Download repo
2. Unzip repo
3. Open in IDE of choice
4. Install all dependencies (listed below)
5. Compile and run slither bot!

### Dependencies ###
* Selenium
* Requests
* Beautiful Soup
* Fuzzywuzzy
* OS
* Tkinter

### How slither bot works ###
Slither bot uses requests/beautiful soup to scrape the given webpage for the names of items. Fuzzy Wuzzy is then used to compare given items with requested item, it finds the "most similar" item and then utalizes selenium to interact with the webpage. Selenium is used to add the item to the users cart, auto fill the users information etc. Slither bot automatically closes the browser window after waiting for 10 seconds after all auto-checkout is complete.

Tkinter is used to create the UI for slither bot. In combination with os and a bit of tkinter slither bot comes prepackaged with a file management system within the UI. It is entirely possible to manage all slither bot tasks through the UI. Each task added to the slither bot task manager (window within the UI) contains a specific item information, user information, and a task name. 

### Default opitons ###
***All items listed below can be editted to suite individual user preference***
By default, slither bot....
* will not fully checkout on any given task (this is left to manual user take over)
* will wait 10 seconds for user input on any given checkout page before closing the window.
* Uses Safari as default browser
* Has one "test profile" and one "test user" to ensure slither bot is working correctly
* In order to run the program, "gui.py" should be run
* Will wait for the drop if it is not 11:00:00 am EST time.

### UI ###
**main UI**
![alt text](https://github.com/Beaninator/Slither-Bot/blob/main/images/main-ui.png "UI-Main")
![alt text](https://github.com/Beaninator/Slither-Bot/blob/main/images/task-populated.png "UI-Populated")

**user creation UI**
![alt text](https://github.com/Beaninator/Slither-Bot/blob/main/images/user-create.png "user-Main")

**item creation UI**
![alt text](https://github.com/Beaninator/Slither-Bot/blob/main/images/item-create.png "item-Main")





