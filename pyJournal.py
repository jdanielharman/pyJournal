from datetime import datetime as dt
import tkinter as tk
import random
import os

class pyJournal():
    # Class Attributes

    def __init__(self):
        ''' pyJournal Constructor '''
        self.filePrefix = r'C:\\Users\\jdhar\\OneDrive\\Personal\\Journal Entries\\' # Location of Entries
        self.fileName   = None                      # Save File Name
        self.dailyFile  = self.__getDailyFile()     # Get today's File
        self.question   = self.__getDailyQuestion() # Get today's Question
        self.isEdited   = False

        self.root       = tk.Tk()                   # Root Window Object
        self.scrollbar  = tk.Scrollbar(self.root)   # Scrollbar Object for Window
        self.textBox    = tk.Text(self.root, yscrollcommand=self.scrollbar.set) # Create Textbox Option
        self.textBox.storeobj = {}
        self.button     = tk.Button(self.root, text='Submit', 
                                    command=self.__submitResponse,
                                    padx = 20, pady = 5) # Create Button
        
        self.__configTk()       # Configure the Window Attributes
        self.root.mainloop()    # Run Window Mainloop
        self.dailyFile.close()  # Close File
        if not self.isEdited: os.remove(self.fileName)

    def __getDailyQuestion(self):
        ''' Return the Daily Question for Today '''
        questionFile = open(r'C:\\Users\\jdhar\\OneDrive\\Projects\\pyJournal\\introspectiveQuestions.txt', 'r', encoding="utf8")
        questions    = [ line for line in questionFile ]
        numLines     = len(questions)
        randNum      = random.randint(0, numLines - 1)
        return questions[randNum]
        
    def __getDailyFile(self):
        ''' Returns the Daily File Object for Today's Date '''
        today = dt.today()  # Get Today's Date 
        month = today.strftime("%b")    # Get the Month as a String
        # Check for Year Dir
        if not os.path.isdir(self.filePrefix + str(today.year)): 
            os.mkdir(self.filePrefix + str(today.year))
        # Check for Month Dir
        if not os.path.isdir(self.filePrefix + str(today.year) + r'\\' + month):
            os.mkdir(self.filePrefix + str(today.year) + r'\\' + month)
        # Create File Name
        self.fileName = self.filePrefix + str(today.year) + r'\\' + month + r'\\' \
                      + f'JDH-{today.month}-{today.day}-{today.year}' + '.txt'
        return open(self.fileName, 'a')  # Return Today's File

    def __submitResponse(self):
        response = self.textBox.get("1.0", tk.END).splitlines() # Save Response

        for line in response:
            self.dailyFile.write(line + '\n')

        # self.dailyFile.write(ret)  # Write Response to File
        self.isEdited = True    # File has been Written to
        self.root.destroy()

    def __configTk(self):
        ''' Configure the Tkinter Window '''
        self.root.geometry("600x400")                   # Set Window Size
        self.root.minsize(height = 560)                 # Set Minimum Height
        self.root.title("pyJournal")                    # Set Window Title
        self.__create_binding_keys()
        self.textBox.tag_configure("sel", background="skyblue")
        self.textBox.storeobj['Copy']           = self.__copy
        self.textBox.storeobj['Cut']            = self.__cut
        self.textBox.storeobj['Paste']          = self.__paste
        self.textBox.storeobj['SelectAll']      = self.__select_all
        self.textBox.storeobj['DeselectAll']    = self.__deselect_all
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)   # Pack Scrollbar onto Window
        self.button.pack(side=tk.BOTTOM)                # Pack Button onto Window
        self.textBox.pack(fill=tk.BOTH)                 # Pack Text Box onto Window
        self.scrollbar.config(command=self.textBox.yview)   # Configure the Scrollbar to Control Text Box
        self.textBox.insert(tk.END, self.question + '\n\n') # Insert Today's Question
        self.textBox.insert(tk.END, 'Daily Recap:\n\n')     # Insert Today's Response
        
    def __copy(self, event):
        self.textBox.event_generate("&lt;&lt;Copy>>")

    def __paste(self, event):
        self.textBox.event_generate("&lt;&lt;Paste>>")

    def __cut(self, event):
        self.textBox.event_generate("&lt;&lt;Cut>>")

    def __create_binding_keys(self):
        for key in ["&lt;Control-a>","&lt;Control-A>"]:
            self.textBox.master.bind(key, self.__select_all)
        for key in ["&lt;Button-1>","&lt;Return>"]:
            self.textBox.master.bind(key, self.__deselect_all)
        return

    def __select_all(self, event):
        self.textBox.tag_add("sel",'1.0','end')
        return

    def __deselect_all(self, event):
        self.textBox.tag_remove("sel",'1.0','end')

if __name__ == '__main__':
    journal = pyJournal()
        
