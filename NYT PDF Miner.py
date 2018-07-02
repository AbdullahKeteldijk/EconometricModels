"""
PDF Miner New York Times Bestsellers

Author: Abdullah Keteldijk
Date: 6-3-2018


"""

from cStringIO import StringIO
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from Tkinter import *
from tkFileDialog import *
import pandas as pd
import os

def convert(path):
    try:
        # Check input values.
        #path = purify(path)
        # Create IO utilities. 
        manager, io = PDFResourceManager(), StringIO()
        # Initiate conversion paramters/Objects.
        codec, params = 'ascii', LAParams()
        device, f = TextConverter(manager, io, codec=codec, laparams=params), file(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)
        # Get PDF pages.
        pages = PDFPage.get_pages(f, set(), maxpages = 0, password = "", caching = True, check_extractable = True)
        for page in pages:
            interpreter.process_page(page)
        # Get PDF text.
        text = io.getvalue()
        # Close iO entities. 
        f.close(), device.close(), io.close()
        return text
    except Exception:
        return ''
'''

'''

def Position(Text, Type):
    TWIndex = -1
    status = 0
    
    for i in range(len(Type)): 
        if i < len(Type):
            if Type[i] == 'This ' and Type[i+1] == 'Week ':
                    TWIndex = i+1
            elif Type[i] == 'Last ' and Type[i+1] == 'Week ':
                LWIndex = i+1

    if TWIndex == -1:
        for i in range(len(Type)):
            if Text[i]== 'This ' and Text[i+1] == 'Week ':
                TWIndex = i+1
                status = 1
            

    
    return [TWIndex, LWIndex, status]

def Numbers(Type, Status):
    
    Weeks = []
    if Status == 0:
        for i in range(len(Type)): 
            if i < len(Type):
                if Type[i] == 'On List ':
                    OnList = i
                if Type[i] == 'Hawes Publications ':
                    End = i
    elif Status == 1:
        for i in range(len(Type)): 
            if i < len(Type):
                if Type[i] == 'Last ' and Type[i+1] == 'Week ' :
                    OnList = i+1
                if Type[i] == 'Hawes Publications ':
                    End = i        
    
    Weeks.append(Type[OnList:End]) # FF goed checken. indexen per 2. Ook date fixen.
    
    return Weeks

def GetCategory(Text):
    for  i in range(len(Text)):
        if Text[i] == 'Fiction ':
            FIndex = i
            Date = Text[i-2]
##            print('F index', FIndex)
        elif Text[i] == 'Non-Fiction ':
            NFIndex = i
##            print('NF index', NFIndex)


    Fiction = []
    for i in range(FIndex+3, NFIndex-6):
        Fiction.append(Text[i])
    
    NonFiction = []
    for i in range(NFIndex+3, len(Text)):
        NonFiction.append(Text[i])
    
    
    [TW_Fiction, LW_Fiction, Status_F] = Position(Text, Fiction)
    [TW_NonFiction, LW_NonFiction, Status_NF] = Position(Text, NonFiction)

    Weeks_F = Numbers(Fiction, 0) #Test voor uitzonderings gevallen 
    Weeks_NF = Numbers(NonFiction, Status_F)

    
    Fiction = []

    if Status_F == 0:
        StartIndex = 8
        EndIndex = TW_Fiction+StartIndex-2
    else:
        StartIndex = FIndex+2
        EndIndex = LW_Fiction + StartIndex
##        print('start', StartIndex, Text[StartIndex])
##        print('end', EndIndex, Text[EndIndex])
        #print('ddd', Text[StartIndex:EndIndex])
    for i in range(StartIndex, EndIndex):
        Fiction.append(Text[i])
    
    NonFiction = []
    for i in range(NFIndex+4, NFIndex+TW_NonFiction+2): ## Index NFIndex = 229 TW_NonFiction = 59
        NonFiction.append(Text[i])

    if Fiction[-1] != ' ' and Fiction[-1] != '':
        Fiction.append(' ')
    if NonFiction[-1] != ' ' and NonFiction[-1] != '':
        NonFiction.append(' ')
        
    return Fiction, NonFiction, Weeks_F, Weeks_NF, Date
    
def GetBooks(Type):
    BookList = []
    Empty = 0

    for i in range(len(Type)):
                 
        if Type[i] == '' or Type[i] == ' ':
            BookList.append(Type[Empty:i])
            Empty  = i
        
    for i in range(len(BookList)):
        try:
            BookList[i].remove(' ')
        except Exception:
            print("list.remove(x): x not in list")
    return BookList

def GetBook(BookList):
    Book = []
    print('len boook: ', len(BookList))
    for i in range(len(BookList)):
        BookList[i] = ' '.join(BookList[i])
    return BookList

def GetInfo(Books):
    
    Title = []
    Author = []
    Publisher = []
    Price = []
    Description = []

    Index2 = 0

    for k in range(len(Books)):
        Book = Books[k]
        Index = 0
        Check1 = 0
        Check2 = 0
        Check3 = 0
        Check4 = 0
        Check5 = 0
        bracet = 0
        dollar = 0

       
        for i in range(len(Book)-3):
            #if i < len(Book):
            if Book[i] == 'b' and Book[i+1] == 'y' and Check1 == 0:
                Title.append(Book[0:i-2])
                Index = i+1
                Check1 = 1
            if i > Index and Book[i] == '.' and Book[i+1] == ' ' and Book[i+2] == '(' and Check2 == 0: ## Extra consitie meegeven ivm brackets

                Author.append(Book[Index+2:i])
                
                Index = i
                Check2 = 1
            elif i > Index and Book[i] == '.' and Book[i+1] == ' ' and Book[i+3] == '(' and Check2 == 0: ## Extra consitie meegeven ivm brackets

                Author.append(Book[Index+2:i])
                
                Index = i
                Check2 = 1
            
            if i > Index and Book[i] == '$' and Check3 == 0:
                Publisher.append(Book[Index+3:i-2])
                Index = i-2
                Check3 = 1

            if i > Index and Book[i] == '$' and Check4 == 0:

                dollar = i+1
                for j in range(Index,Index+30):
                    if Book[j] == ' 'and Book[j+1] == ')':
                        bracet = j
                       
                    elif Book[j] == '.' and Book[j+1] == ')':
                        bracet = j
                        
                               
                Price.append(Book[dollar:bracet])
            
                Index = bracet
                Check4 = 1 
                

            if i > Index and Check4 == 1 and Check5 == 0:
                
                Description.append(Book[Index+3:-2])
                Check5 = 1
##    print('hjgyg; ', Books[-1])
    for i in range(len(Description)): #Removing spaces from the beginning of the sentence
        Description[i] = " ".join(Description[i].split())

            
    return Title, Author, Publisher, Price, Description
                       
def GetWeeks(Weeks, BookList):
    LastWeek = []
    OnList = []
    ThisWeek = []

    for i in range(len(Weeks)):
        if Weeks[i] != '' and Weeks[i] != ' ' and Weeks[i] != 'On List ' and len(LastWeek) < len(BookList): 
            if Weeks[i] == '-- ': 
                LastWeek.append('0')
            else:
                LastWeek.append(Weeks[i])
        elif Weeks[i] != '' and Weeks[i] != ' ' and Weeks[i] != 'On List ':
            if Weeks[i] == '-- ':
                OnList.append('0')
            else:
                OnList.append(Weeks[i])


##    print('1LastWeek: ', (LastWeek))
##    print('OnList: ', (OnList))
##    print('LastWeek: ', len(LastWeek))
##    print('OnList: ', len(OnList))

    CountBooks = (len(LastWeek) + len(OnList))/2
    if len(LastWeek) > len(OnList):
        diff = len(LastWeek) - CountBooks
        if diff >1:
            values = LastWeek[len(LastWeek)-diff-1:-1]
            del LastWeek[len(LastWeek)-diff-1:-1]
            OnList = values + OnList
        else:
            values = [LastWeek[-1]]
            del LastWeek[-1]
            OnList = values + OnList
    elif len(LastWeek) < len(OnList):
        diff = len(OnList) - CountBooks
        if diff >1:
            values = OnList[0:diff]
            del OnList[0:diff]
            LastWeek = LastWeek + values 
        else:
            values = [OnList[0]]
            del OnList[0]
            LastWeek = LastWeek + values 

##    try:
##        print('Diff: ', diff, 'Values', values)
##    except Exception:
##        print('')
##    
##    print('2LastWeek: ', (LastWeek))
##    print('OnList: ', (OnList))
##    print('LastWeek: ', len(LastWeek))
##    print('OnList: ', len(OnList))
        
    for i in range(len(LastWeek)):
        LastWeek[i] = LastWeek[i].replace(' ', '')
        OnList[i] = OnList[i].replace(' ', '')

    if 'Week' in LastWeek:
        LastWeek.remove('Week')
    if 'Weeks' in OnList:
        OnList.remove('Weeks')
    
    for i in range(len(LastWeek)):
        ThisWeek.append(i+1)

##    print('Last ', LastWeek)
##    print('Onlist ', OnList)
    return LastWeek, OnList, ThisWeek

def GetDate(Date, CountBooks):
    Date = Date.split()
    Month = {
        'January': 1,
        'Februari': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'Juli': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12}
  
    Date[0] = str(Month[Date[0]])
    
    Date[1] = Date[1].replace(',','')
    Date[2] = Date[2]
    Date = Date[0] + '-' + Date[1] + '-' + Date[2]

    NewDate = []
    for i in range(0, CountBooks):
        NewDate.append(Date)
    return NewDate

def GetType(BookList_F, BookList_NF):

    AllTypes = []

    for i in range(len(BookList_F)):
        AllTypes.append("Fiction")
    for i in range(len(BookList_NF)):
        AllTypes.append("NonFiction")  

    return  AllTypes   

def GetTable(Data_F, Data_NF, Types, Dates):

    for i in range(len(Data_F)):
        for j in range(len(Data_NF[i])):
            Data_F[i].append(Data_NF[i][j])

    Data = Data_F

    print('Date', len(Dates))
    print('ThisWeek', len(Data[7]))
    print('Title', len(Data[0]))
    print('Author', len(Data[1]))
    print('Publisher', len(Data[2]))
    print('Price', len(Data[3]))
    print('Description', len(Data[4]))
    print('LastWeek', len(Data[5]))
    print('OnList', len(Data[6]))
    print('Types', len(Types))
    
    
    Info = [('Date', Dates),
            ('ThisWeek', Data[7]),
            ('Title',Data[0]),
            ('Author', Data[1]),
            ('Publisher', Data[2]),
            ('Price', Data[3]),
            ('Description', Data[4]),
            ('LastWeek', Data[5]),
            ('OnList', Data[6]),
            ('Types', Types)]

    df = pd.DataFrame.from_items(Info)

    return df

def PDFMiner(File, count):
    path = "C:\\Users\\srema\\Documents\\Master Thesis\\NYT\\" + File
    Text = convert(path).split('\n')

##    print(Text)
    
    [Fiction, NonFiction, Weeks_F, Weeks_NF, Date] = GetCategory(Text)

    Weeks_F = Weeks_F[0]
    Weeks_NF = Weeks_NF[0]
    
    BookList_F = GetBooks(Fiction)
    BookList_NF = GetBooks(NonFiction)

##    print("KKK: ", NonFiction)

    [LastWeek_F, OnList_F, ThisWeek_F] = GetWeeks(Weeks_F, BookList_F)
    [LastWeek_NF, OnList_NF, ThisWeek_NF] = GetWeeks(Weeks_NF, BookList_NF)    

    BookList_F = GetBook(BookList_F)
    BookList_NF = GetBook(BookList_NF)
    

##    print('Length BLF', len(BookList_F))
##    print('Length BLNF', len(BookList_F))
    
    [Title_F, Author_F, Publisher_F, Price_F, Description_F] = GetInfo(BookList_F)
    [Title_NF, Author_NF, Publisher_NF, Price_NF, Description_NF] = GetInfo(BookList_NF)

##    print("Author F: ", Author_F)
##    print("Author NF: ", Author_NF)
##    print("Titles F: ", len(Title_F))
##    print("Titles NF: ", len(Title_NF))
##    print("Author F: ", len(Author_F))
##    print("Author NF: ", len(Author_NF))
##    print("Publisher F: ", len(Publisher_F))
##    print("Publisher NF: ", len(Publisher_NF))
##    print("Price F: ", len(Price_F))
##    print("Price NF: ", len(Price_NF))
##    print("Description F: ", len(Description_F))
##    print("Description NF: ", len(Description_NF))
    
    Data_F = [Title_F, Author_F, Publisher_F, Price_F, Description_F, LastWeek_F, OnList_F, ThisWeek_F]
    Data_NF = [Title_NF, Author_NF, Publisher_NF, Price_NF, Description_NF, LastWeek_NF, OnList_NF, ThisWeek_NF]

##    print("Data F: ", len(Data_F))
##    print("Data NF: ", len(Data_NF))
    
    Types = GetType(Title_F, Title_NF)
    CountBooks = len(Title_F) + len(Title_NF)
    Dates = GetDate(Date, CountBooks)
##    print("Types: ", len(Types))
##    print("Dates: ", len(Dates))
    
    Table = GetTable(Data_F, Data_NF, Types, Dates)
    
    Table.to_csv("C:\\Users\\srema\\Documents\\Master Thesis\\NYT\\Datasets\\NewYorkTimes Bestsellers " + File + ".csv", index=False)
    print("Processed: ", count)

def main():

    Files = os.listdir("C:\\Users\\srema\\Documents\\Master Thesis\\NYT")

    #PDFMiner(Files[4], 5)
    for i in range(len(Files)):
        try:
            PDFMiner(Files[i], i+1)
        except Exception:
            print('Error: ', File[i])
     




## pandas dataframe
## http://pbpython.com/pandas-list-dict.html
## http://www.hawes.com/pastlist.htm    


if __name__ == '__main__':
    main()
    print("Done")
 
