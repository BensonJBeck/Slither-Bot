import tkinter as tk
from os import listdir
from os.path import join, isfile
from tkinter import *
from bot_main import *

taskQueue = []

textColor = '#BDBDBD'
mainBG = '#464646'
frameBG = '#2D2D2D'
deleteBG = '#B22222'

current_user = {
    "name": "",
    "email": "",
    "phone": "",
    "address": "",
    "zipCode": "",
    "city": "",
    "cardNumber": "",
    "cvv": "",
    "month": "",
    "year": "",
    "phone": ""
}

current_item = {
    "name": "",
    "type": "",
    "color_way": "",
    "size": ""
}


def mainWindow():
    version = 1.2
    window = tk.Tk()
    window.resizable(height=FALSE, width=FALSE)
    window.title("Supreme Bot Version " + str(version))
    window.geometry('465x325')
    window.configure(bg=mainBG)

    # FRAME 1
    taskFrameLBL = Label(text='New Task', font=('Helvetica', 16, 'bold'), foreground=textColor, bg=mainBG)
    taskFrame = Frame(window, bg=frameBG)

    nameLabel = Label(taskFrame, text='TASK NAME', bg=frameBG, foreground=textColor)
    userLabel = Label(taskFrame, text='USER PROFILE', bg=frameBG, foreground=textColor)
    itemLabel = Label(taskFrame, text='ITEM PROFILE', bg=frameBG, foreground=textColor)

    createUProfileBTN = Button(taskFrame, text='Create New User', command=lambda: generateUserWindow(taskFrame),
                               highlightbackground=frameBG)
    createIProfileBTN = Button(taskFrame, text='Create New Item', command=lambda: generateProfileWindow(taskFrame),
                               highlightbackground=frameBG)

    taskNameEnt = Entry(taskFrame, bg=mainBG, foreground=textColor)

    users = getUsers()
    uValue = StringVar(taskFrame, users[len(users) - 1])
    useOpt = OptionMenu(taskFrame, uValue, *users)
    useOpt.configure(bg=frameBG)

    profiles = getProfileOptions()
    pValue = StringVar(taskFrame, profiles[len(profiles) - 1])
    profOpt = OptionMenu(taskFrame, pValue, *profiles)
    profOpt.configure(bg=frameBG)

    supportedWebDrivers = ['Safari', 'Chrome', 'Firefox', 'Internet Explorer']
    wValue = StringVar(taskFrame, supportedWebDrivers[0])
    wOpt = OptionMenu(taskFrame, wValue, *supportedWebDrivers)
    wOpt.configure(bg=frameBG)

    nameLabel.grid(row=0, column=0, sticky=tk.W, pady=3)
    taskNameEnt.grid(row=1, column=0)
    userLabel.grid(row=2, column=0, sticky=tk.W, pady=3)
    useOpt.grid(row=3, column=0, sticky=tk.W)
    itemLabel.grid(row=4, column=0, sticky=tk.W)
    profOpt.grid(row=5, column=0, sticky=tk.W, pady=5)
    createUProfileBTN.grid(row=6, column=0, sticky=tk.W, pady=5)
    createIProfileBTN.grid(row=7, column=0, sticky=tk.W, pady=5)
    wOpt.grid(row=8, column=0, sticky=tk.W, pady=5)

    # FRAME 2
    monitorFrameLBL = Label(text='Task Monitor', font=('Helvetica', 16, 'bold'), foreground=textColor, bg=mainBG)
    monitorFrame = Frame(window, bg=frameBG)
    taskListBox = Listbox(
        monitorFrame,
        width=25,
        height=15,
        fg=mainBG,
        selectbackground='#A7C7E7',
        bg=frameBG)

    startTasksBTN = Button(monitorFrame, text='Start Tasks', command=lambda: start_tasks(wValue.get()),
                           highlightbackground=frameBG)

    deleteTaskBTN = Button(monitorFrame, text='Delete', command=lambda: deleteTask(taskListBox),
                           highlightbackground=frameBG)
    createTaskBTN = Button(monitorFrame, text='Add Task',
                           command=lambda: addTask(taskListBox, taskNameEnt.get(), pValue.get(), uValue.get()),
                           highlightbackground=frameBG)

    taskListBox.grid(row=0, column=0, columnspan=3)
    createTaskBTN.grid(row=1, column=0)
    deleteTaskBTN.grid(row=1, column=1)
    startTasksBTN.grid(row=1, column=2)

    taskFrameLBL.grid(row=0, column=0, pady=5)
    taskFrame.grid(row=1, column=0, padx=15)

    monitorFrameLBL.grid(row=0, column=1, pady=5)
    monitorFrame.grid(row=1, column=1)

    window.mainloop()


def generateProfileWindow(taskFrame):
    window = tk.Tk()
    window.title("Item Profile Creator")
    window.resizable(0, 0)
    window.configure(bg=mainBG)

    window.columnconfigure(0, minsize=200, weight=1)

    name = _default_name()
    profile_name = Label(window, text="Profile Name:", bg=mainBG, fg=textColor)
    profile_name.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    profile_entry = Entry(window)
    profile_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
    profile_entry.insert(END, name)

    # item name
    name_label = Label(window, text="Item Name:", bg=mainBG, fg=textColor)
    name_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    name_entry = Entry(window)
    name_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

    # item color label
    color_label = Label(window, text="Item Color:", bg=mainBG, fg=textColor)
    color_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

    color_entry = Entry(window)
    color_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

    # item size label
    item_size_label = Label(window, text="Item Size:", bg=mainBG, fg=textColor)
    item_size_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

    options = [
        "X-Small",
        "Small",
        "Medium",
        "Large",
        "X-Large"
    ]
    size_value = StringVar(window, options[2])

    size_entry = OptionMenu(window, size_value, *options)
    size_entry.configure(bg=frameBG)
    size_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

    # item type label
    type_label = Label(window, text="Item Type:", bg=mainBG, fg=textColor)
    type_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

    type_options = [
        "t-shirt",
        "jacket",
        "shirt",
        "sweater",
        "pant",
        "bag",
        "accessory",
        "shoe"
    ]
    type_value = StringVar(window, type_options[0])
    type_entry = OptionMenu(window, type_value, *type_options)
    type_entry.configure(bg=frameBG)
    type_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    submit_button = Button(window, text='Create Profile',
                           command=lambda: write_item_profile(profile_entry.get(), name_entry.get(), type_value.get(),
                                                              color_entry.get(), size_value.get(), taskFrame),
                           highlightbackground=frameBG)
    submit_button.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

    window.mainloop()


def generateUserWindow(taskFrame):
    window = tk.Tk()
    window.title("Item Profile Creator")
    window.resizable(0, 0)
    window.configure(bg=mainBG)

    name = Label(window, text="Profile Name:", bg=mainBG, foreground=textColor)
    email = Label(window, text="Email:", bg=mainBG, foreground=textColor)
    address = Label(window, text="Address:", bg=mainBG, foreground=textColor)
    zip = Label(window, text="Zip-code:", bg=mainBG, foreground=textColor)
    city = Label(window, text="City:", bg=mainBG, foreground=textColor)
    cardNumber = Label(window, text="Card Number:", bg=mainBG, foreground=textColor)
    expMonth = Label(window, text="Expiration Month:", bg=mainBG, foreground=textColor)
    expYear = Label(window, text="Expiration Year:", bg=mainBG, foreground=textColor)
    CVV = Label(window, text="CVV:", bg=mainBG, foreground=textColor)
    phone = Label(window, text="Telephone Number:", bg=mainBG, foreground=textColor)
    labels = [name, email, address, zip, city, cardNumber, expMonth, expYear, CVV, phone]

    phoneENT = Entry(window)
    nameENT = Entry(window)
    emailENT = Entry(window)
    addressENT = Entry(window)
    zipENT = Entry(window)
    cityENT = Entry(window)
    cardNumberENT = Entry(window)
    expMonthENT = Entry(window)
    expYearENT = Entry(window)
    CVVENT = Entry(window)
    entries = [nameENT, emailENT, addressENT, zipENT, cityENT, cardNumberENT, expMonthENT, expYearENT, CVVENT, phoneENT]

    for row in range(len(labels)):
        labels[row].grid(row=row, column=0)
        entries[row].grid(row=row, column=1)

    createUProfileBTN = Button(window, text='Create',
                               command=lambda: write_user_profile(nameENT.get(), emailENT.get(), addressENT.get(),
                                                                  zipENT.get(), cityENT.get(), cardNumberENT.get(),
                                                                  expMonthENT.get(), expYearENT.get(), CVVENT.get(), phoneENT.get(),
                                                                  taskFrame), highlightbackground=frameBG)
    createUProfileBTN.grid(row=(len(labels) + 1), column=1, pady=5)


def getProfileOptions():
    workingPath = os.getcwd() + "/item_profiles"
    profiles = [f for f in listdir(workingPath) if isfile(join(workingPath, f))]
    return profiles


def getUsers():
    workingPath = os.getcwd() + "/user_profiles"
    profiles = [f for f in listdir(workingPath) if isfile(join(workingPath, f))]
    return profiles
    pass


def _default_name():
    workingPath = os.getcwd() + "/item_profiles"
    file_count = 0
    for path in os.listdir(workingPath):
        if os.path.isfile(os.path.join(workingPath, path)):
            file_count += 1
    name = "profile" + str(file_count)
    return name


def addTask(taskListBox, processName, itemName, userName):
    taskListBox.insert(END, processName)
    read_item_profile(itemName)
    read_user_profile(userName)
    print(current_user)
    print(current_item)
    task = [processName, current_item, current_user]
    taskQueue.append(task)


def deleteTask(taskListBox):
    taskListBox.delete(ANCHOR)


def write_item_profile(profile_entry, name_entry, type_value, color_entry, size_value, taskFrame):
    item_profile = {"file-name": profile_entry, "item-name": name_entry, "item-type": type_value,
                    "item-color": color_entry, "item-size": size_value}
    workingPath = os.getcwd() + "/item_profiles/" + item_profile["file-name"]
    file = open(workingPath, "w")

    for key, value in item_profile.items():
        file.write('%s:%s\n' % (key, value))
    file.close()
    update_menus(taskFrame)


def write_user_profile(name, email, address, zip, city, cardNum, month, year, cvv, phone, taskFrame):
    user_profile = {"file-name": name, "email": email, "address": address,
                    "zip": zip, "city": city, "card-number": cardNum, "EXP-month": month,
                    "EXP-year": year, "CVV": cvv, "phone":phone}
    workingPath = os.getcwd() + "/user_profiles/" + user_profile["file-name"]
    file = open(workingPath, "w")

    for key, value in user_profile.items():
        file.write('%s:%s\n' % (key, value))

    file.close()
    update_menus(taskFrame)
    pass


def update_menus(taskFrame):
    users = getUsers()
    uValue = StringVar(taskFrame, users[len(users) - 1])
    useOpt = OptionMenu(taskFrame, uValue, *users)
    useOpt.configure(bg=frameBG)

    profiles = getProfileOptions()
    pValue = StringVar(taskFrame, profiles[len(profiles) - 1])
    profOpt = OptionMenu(taskFrame, pValue, *profiles)
    profOpt.configure(bg=frameBG)

    useOpt.grid(row=3, column=0, sticky=tk.W)
    profOpt.grid(row=5, column=0, sticky=tk.W)


def read_item_profile(itemFile):
    workingPath = os.getcwd() + "/item_profiles/" + itemFile
    try:
        file = open(workingPath, "r")
        for words in file:
            line = words.rstrip('\n').split(":")
            attribute = line[0]
            value = line[1]
            if attribute == "item-name":
                current_item["name"] = value
            if attribute == "item-type":
                current_item["type"] = value
            if attribute == "item-color":
                current_item["color_way"] = value
            if attribute == "item-size":
                current_item["size"] = value
    except:
        print("Item profile not found")
    print(current_item)


def read_user_profile(itemFile):
    workingPath = os.getcwd() + "/user_profiles/" + itemFile
    try:
        file = open(workingPath, "r")
        for words in file:
            line = words.rstrip('\n').split(":")
            attribute = line[0]
            value = line[1]
            if attribute == "file-name":
                current_user["name"] = value
            if attribute == "email":
                current_user["email"] = value
            if attribute == "address":
                current_user["address"] = value
            if attribute == "zip":
                current_user["zipCode"] = value
            if attribute == "city":
                current_user["city"] = value
            if attribute == "card-number":
                current_user["cardNumber"] = value
            if attribute == "EXP-month":
                current_user["month"] = value
            if attribute == "EXP-year":
                current_user["year"] = value
            if attribute == "CVV":
                current_user["cvv"] = value
            if attribute == "phone":
                current_user["phone"] = value
    except:
        print("Item profile not found")
    print(current_user)


def start_tasks(browser):
    for task in taskQueue:
        item = task[1]
        user = task[2]
        cart_item(item, user, browser)


mainWindow()
