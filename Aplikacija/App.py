from tkinter import Tk, ttk, Button, Label, Entry, messagebox, Checkbutton, LabelFrame, Scrollbar, filedialog, END, IntVar
from Parser import Parser
from datetime import date
import os

def LoadFile():
    path = os.getcwd()
    filename = filedialog.askopenfilename(initialdir=path, title="Odaberite datoteku", filetypes=[("Text files","*.txt")])
    
    if len(filename) > 0:
        try:
            parser.ClearData()
            parser.SetFilename(filename)
            splitFilename = filename.split("/")
            loadedFileLabel.config(text = splitFilename[len(splitFilename)-1])
            FillDataTable(parser.DataFrame)
            DisplayStatistics()
            messagebox.showinfo("Uspjeh!", "Datoteka učitana!")
        except:
            messagebox.showwarning("Greška", "Datoteka nije pronađena!")
    else:
        messagebox.showwarning("Greška", "Unesite naziv datoteke!")

def ClearDataTable():
    dataTable.delete(*dataTable.get_children())

def FillDataTable(dataFrame):
    ClearDataTable()
    dataTable["column"] = list(dataFrame.columns)
    dataTable["show"] = "headings"
    for column in dataTable["columns"]:
        dataTable.heading(column, text=column)

    dataFrameRows = dataFrame.to_numpy().tolist()
    for row in dataFrameRows:
        dataTable.insert("", "end", values=row)

def SearchData():
    term = searchInput.get()
    if len(term) > 0 and len(parser.dataFrameList) > 0:
        newDataFrame = parser.SearchDataFrame(term)
        FillDataTable(newDataFrame)

def DisplayStatistics():
    statisticsDict = parser.GetStatistics()

    recordsText = "Broj zapisa: " + statisticsDict["records"]
    megabytesText = "Ukupna količina prijenosa: " + statisticsDict["mbytes"] + " MB"
    uniqueText = "Broj jedinstvenih IP adresa: " + statisticsDict["uniqueIPs"]
    topText = "Najčešća IP adresa: " + statisticsDict["topIP"]

    amountOfRecordsLabel.config(text=recordsText)
    megabytesLabel.config(text=megabytesText)
    uniqueIPsLabel.config(text=uniqueText)
    topIPLabel.config(text=topText)

def DisplayGraph():
    graphValues = {
                    "Udio po HTTP odgovoru": 0,
                    "Udio po metodi": 1,
                    "Količina zahtjeva po danu": 2
                }
    if len(parser.dataFrameList) > 0:
        parser.DisplayGraph(graphValues[graphsCombobox.get()])
        window.quit()

def SaveData():
    pass

#------------------------------------------------parser------------------------------------------------
parser = Parser()
newDataFrame = None

#------------------------------------------------window------------------------------------------------
window = Tk()
window.geometry("1200x800+250+50")
window.resizable(0, 0)
window.title("Log parser")

#----------------------------------------------fileselect----------------------------------------------
fileFrame = LabelFrame(window, text="Odabir datoteke:", height=94, width=200, borderwidth=2, relief="groove")
fileFrame.place(x=5, y=0)

filenameLabel = Label(fileFrame, text="Naziv datoteke:")
filenameLabel.place(x=10, y=5)

loadedFileLabel = Label(fileFrame, text="/", foreground="red")
loadedFileLabel.place(x=95, y=5)

filenameButton = Button(fileFrame, text="Učitaj datoteku", command=LoadFile)
filenameButton.place(x=50, y=35)

#----------------------------------------------checkboxes----------------------------------------------
varClientIP = IntVar()
varClientID = IntVar()
varUsername = IntVar()
varDate = IntVar()
varContent = IntVar()
varHTTP = IntVar()
varBytes = IntVar()
varRef = IntVar()
varAgent = IntVar()

checkboxesFrame = LabelFrame(window, text="Odabir polja:", height=120, width=600, borderwidth=2, relief="groove")
checkboxesFrame.place(x=205, y=0)

refreshButton = Button(window, text="Osvježi prikaz")
refreshButton.place(x=310, y=100)

clientIPCheckbox = Checkbutton(checkboxesFrame, text="IP klijenta", variable=varClientIP)
clientIPCheckbox.grid(row=0, column=0)
clientIPCheckbox.select()

clientIDCheckbox = Checkbutton(checkboxesFrame, text="ID korisnika", variable=varClientID)
clientIDCheckbox.grid(row=1, column=0)
clientIDCheckbox.select()

usernameCheckbox = Checkbutton(checkboxesFrame, text="Korisničko ime", variable=varUsername)
usernameCheckbox.grid(row=2, column=0)
usernameCheckbox.select()

dateCheckbox = Checkbutton(checkboxesFrame, text="Datum", variable=varDate)
dateCheckbox.grid(row=0, column=1)
dateCheckbox.select()

contentCheckbox = Checkbutton(checkboxesFrame, text="Sadržaj", variable=varContent)
contentCheckbox.grid(row=1, column=1)
contentCheckbox.select()

httpCheckbox = Checkbutton(checkboxesFrame, text="HTTP status", variable=varHTTP)
httpCheckbox.grid(row=2, column=1)
httpCheckbox.select()

bytesCheckbox = Checkbutton(checkboxesFrame, text="Količina bajtova", variable=varBytes)
bytesCheckbox.grid(row=0, column=2)
bytesCheckbox.select()

refCheckbox = Checkbutton(checkboxesFrame, text="Refereer", variable=varRef)
refCheckbox.grid(row=1, column=2)
refCheckbox.select()

agentCheckbox = Checkbutton(checkboxesFrame, text="Agent", variable=varAgent)
agentCheckbox.grid(row=2, column=2)
agentCheckbox.select()

#------------------------------------------------search------------------------------------------------
searchLabel = Label(window, text="Pretraga:")
searchLabel.place(x=10, y=330)

searchInput = Entry(window, width=20, highlightcolor="red", highlightthickness=1)
searchInput.place(x=65, y=330)

searchButton = Button(window, text="Pretraži", command=SearchData)
searchButton.place(x=200, y=327)

#-----------------------------------------------datatable----------------------------------------------
dataFrame = LabelFrame(window, text="Sadržaj datoteke:")
dataFrame.place(height=400, width=1200, x=0, y=360)

dataTable = ttk.Treeview(dataFrame)
dataTable.place(relheight=1, relwidth=1)

dataTableBarX = Scrollbar(dataFrame, orient="horizontal", command=dataTable.xview)
dataTableBarY = Scrollbar(dataFrame, orient="vertical", command=dataTable.yview)
dataTable.configure(xscrollcommand=dataTableBarX.set, yscrollcommand=dataTableBarY.set)
dataTableBarX.pack(side="bottom", fill="x")
dataTableBarY.pack(side="right", fill="y")

#----------------------------------------------statistics----------------------------------------------
statisticsFrame = LabelFrame(window, text="Statistika:", height=120, width=257, borderwidth=2, relief="groove")
statisticsFrame.place(x=5, y=140)

amountOfRecordsLabel = Label(statisticsFrame, text="Broj zapisa: /")
amountOfRecordsLabel.place(x=5, y=10)

megabytesLabel = Label(statisticsFrame, text="Ukupna količina prijenosa: /")
megabytesLabel.place(x=5, y=30)

uniqueIPsLabel = Label(statisticsFrame, text="Broj jedinstvenih IP adresa: /")
uniqueIPsLabel.place(x=5, y=50)

topIPLabel = Label(statisticsFrame, text="Najčešća IP adresa: /")
topIPLabel.place(x=5, y=70)

#------------------------------------------------graphs------------------------------------------------
graphsFrame = LabelFrame(window, text="Grafovi:", height=120, width=257, borderwidth=2, relief="groove")
graphsFrame.place(x=262, y=140)

comboboxValues = ["Udio po HTTP odgovoru", "Udio po metodi", "Količina zahtjeva po danu"]
graphsCombobox = ttk.Combobox(graphsFrame, values=comboboxValues)
graphsCombobox.current(0)
graphsCombobox.place(x=55, y=25)

graphsButton = Button(graphsFrame, text="Generiraj graf", command=DisplayGraph)
graphsButton.place(x=85, y= 55)

#-------------------------------------------------save-------------------------------------------------
quitButton = Button(window, text="Spremi podatke", command=SaveData)
quitButton.place(x=1010, y=770)

#-------------------------------------------------quit-------------------------------------------------
quitButton = Button(window, text="Izlaz", width=10, command=window.quit)
quitButton.place(x=1110, y=770)

window.mainloop()