#!/usr/bin/env python
# coding: utf-8

# <p class="pull-left">
# ANLT 224_01 - Data Wrangling
# </p>
# <div class="pull-right">
# <ul class="list-inline">
# Copyright © Trang Vu 2020
# </ul>
# </div>

# <font color='Navy' size=3><em> Trang Vu - 989357826<br>
# HW Week 2 # Regular Expression - Syllabi Feature Assignment </em>

# # Regular Expression - Syllabi Feature Assignment

# In[121]:


# Importing required modules
import PyPDF2
import os
import re
import pandas as pd


# In[122]:


# Locate the folder storing syllabus
# Create a list and store all syllabus in that folder to a list with pathname
dirListing = os.listdir('/Users/trangvu/Desktop/syllabi/')
listFiles = []
for item in dirListing:
    if ".pdf" in item:
        listFiles.append('/Users/trangvu/Desktop/syllabi/'+item)
print (listFiles)


# In[123]:


len(listFiles)


# In[124]:


#listFiles = listFiles[1:20]


# In[ ]:


# Loop through the directories to open all the PDF files
# extract all the pages and texts
# Loop through each page to find desirable matching value
# append to a list
# store in a corresponding key and syllabi in predefined Dictionary

from itertools import chain

Dict = []


for k in range(len(listFiles)):
    # Create a list of different information we would want to retrieve later
    phone = []
    email = []
    website = []
    textbook = []
    homework = []
    prof = []
    location = []
    prep = []
    policy = []
    officehour = []
    descrip = []
    final = []
    
    with open(listFiles[k], 'rb') as pdfFileObj:
        pdfFileObj.seek(0)# Changes here
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
        if pdfReader.isEncrypted:
                pdfReader.decrypt('')
        for i in range(0 ,pdfReader.numPages): 
            num_pages = pdfReader.numPages
            pageObj = pdfReader.getPage(i)
            text  = pageObj.extractText()
            content = [x.replace('\n', ' ') for x in text]
            content = "".join(content)

            # Find phone number for contactting in different syllabus
            regex = re.compile('(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4}|^\d{3}-\d{3}-\d{4}$)')
            phone.append(regex.findall(content))
            
            # Find email for contactting in different syllabus   
            regex2 = re.compile('([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')
            email.append(regex2.findall(content))
        
            # Find webpage for contactting/information in different syllabus
            regex3 = re.compile('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
            website.append(regex3.findall(content))
            
            # Let's find all the textbooks as well as course materials in those syllabuses
            regex4= re.compile('Textbook\s[A-Za-z," ]+|[A-Za-z," ]+Reading\s[A-Za-z," ]+|Textbooks\s\s[A-Za-z," ]+| [A-Za-z," ]+Reading\s[A-Za-z," ]+|Textbook Readings\s[A-Za-z," ]+| [A-Za-z," ]+Course Materials\s[A-Za-z," ]+|Course Materials Required:\s\s[A-Za-z0-9," ]+|Text:\s[A-Za-z0-9," ]+|Texts:\s[A-Za-z0-9," ]+|Course Text\(s\)\s[A-Za-z0-9," ]+')
            textbook.append(regex4.findall(content))
            
            # Let's search for their homework and assignment requirement.
            regex5= re.compile('Homework\s[A-Za-z," ]+|[A-Za-z," ]+Homeworks:\s[A-Za-z," ]+|[A-Za-z," ]+Homework\sassignments\s[A-Za-z," ]+| [A-Za-z," ]+Assignments\s[A-Za-z," ]+|[A-Za-z," ]+Late\sAssignments\s[A-Za-z," ]+')
            homework.append(regex5.findall(content))
            
            #Name of the instructors
            regex6 = re.compile('Professor\s[A-Za-z," ]+|Instructor:\s[A-Za-z\." ]+|Professor :[A-Za-z," ]+|Instructor:[A-Za-z\." ]+|Instructor\'s Name\s:A-Za-z\." ]+|Instructors\s\s[A-Za-z\." ]+|[A-Za-z," ]+Professor\s[A-Za-z," ]+')
            prof.append(regex6.findall(content))
            
            #Room and Office Location
            regex7 = re.compile('Room\s\s[0-9A-Za-z\.," ]+|Office\sLocation:\s\s[0-9A-Za-z\,," ]+|Office\sLocation:\s[A-Za-z," ]+|Office:\s\s[A-Za-z0-9A-Z, "]+|Main\sLocation:\s[A-Za-z," ]+|Office:\s\sRoom\s[[0-9A-Za-z\,\.A-Z," ]]')
            location.append(regex7.findall(content))
            
            # Prerequisite
            regex8 = re.compile('Prerequisite.\s[A-Za-z\.," ]+|Prerequisites:\s[A-Za-z0-9\.," ]+|Prerequisites or Other Requirements\:\s[A-Za-z," ]+|Prerequisites\s:\s[A-Za-z0-9\., "]+')
            prep.append(regex8.findall(content))
            
            # Policy of the courses
            regex9 = re.compile('[A-za-z, "]+\sPolicy\s[A-Za-z\.," ]+|[A-za-z, "]+\sPolicy:\s[A-Za-z\.," ]+|[A-za-z, "]+\sPolicy:\s\s[A-Za-z\.," ]+')
            policy.append(regex9.findall(content))
            
            # Office Hours
            regex10 = re.compile('Office Hours\:\s\s[A-Za-z\/\,0-9\:\-a-z, "]+|Office Hours\s\:\s[A-Za-z\,0-9\:\-a-z, "]+|Office hours\s\s[A-Za-z\,0-9\:\-a-z, "]+|[A-Za-z, "]\soffice\shours\s\s[A-Za-z\,0-9\:\-a-z, "]+|Hours\:\s[A-Za-z\/\,0-9\:\-a-z, "]+')
            officehour.append(regex10.findall(content))
            
            # Course Description
            regex11 = re.compile('[A-za-z, "]+\sDescription:\s[A-Za-z\-0-9, "]+|Course\sDescription:\s[A-Za-z, "]+|[A-za-z, "]+\sDescription\s:\s[A-Za-z\-0-9, "]+|Course\sInformation\s:\s[A-Za-z\-0-9, "]+|Course\sDescription\s\s[A-Za-z\-0-9, "]+')
            descrip.append(regex11.findall(content))
            
            # Final exam notice
            regex12 = re.compile('Final\sExam\:\s[A-Za-z\.," ]+|Final\sExam\s[A-Za-z0-9\%\:," ]+|Final\sexam\:\s[A-Za-z\.," ]+|Final\sexam\s[A-Za-z0-9\%\.," ]+')
            final.append(regex12.findall(content))
             
            #Remove empty string from the output        
            while '' in phone[i]:
                phone.remove('')
            while '' in email[i]:
                email.remove('')
            while '' in website[i]:
                website.remove('')
            while '' in textbook[i]:
                 textbook.remove('')
            while '' in homework[i]:
                 homework.remove('')
            while '' in prof[i]:
                 prof.remove('')
            while '' in location[i]:
                 location.remove('')
            while '' in prep[i]:
                  prep.remove('')
            while '' in policy[i]:
                  policy.remove('')
            while '' in officehour[i]:
                   officehour.remove('')
            while '' in descrip[i]:
                   descript.remove('')
            while '' in final[i]:
                    final.remove('')
                                  
            # Unique function to get only unique email address
            email2 = []
            for x in email:
                if x not in email2:
                    email2.append(x)
             # Unique function to get only unique website address
            website2 = []
            for x in website:
                if x not in website2:
                    website2.append(x)
            
     # Store each output features of each Syllabi into Dictionary for that particular syllabi               
    Dict.append({'Name': listFiles[k], 'Phone':str(list(chain(*phone)))[1:-1],'Email':str(list(chain(*email2)))[1:-1],'Website':str(list(chain(*website2)))[1:-1],'Textbook':str(list(chain(*textbook)))[1:-1],'Homework':str(list(chain(*homework)))[1:-1],'Professor':str(list(chain(*prof)))[1:-1],'Location':str(list(chain(*location)))[1:-1],'Prequisite':str(list(chain(*prep)))[1:-1],'Policy':str(list(chain(*policy)))[1:-1],'Office Hour':str(list(chain(*officehour)))[1:-1],'Description':str(list(chain(*descrip)))[1:-1],'Final':str(list(chain(*final)))[1:-1]})
        
pdfFileObj.close()


# In[114]:


# Now that we have the Dictionary
# Let's turn it into a pandas dataframe
# Rearrange our columns orders
myData =  pd.DataFrame.from_dict(Dict)
myData = myData[['Name', 'Phone', 'Email','Professor','Website','Prequisite','Location','Office Hour','Textbook','Homework','Final','Description','Policy']]
cols = myData.columns.tolist()
cols


# In[115]:


pd.options.display.max_colwidth = 500


# In[116]:


# Take a glance at our dataset
myData.head()


# In[119]:


import csv


# In[120]:


# Export our table into csv file under the same folder with other syllabus path. 
export_csv = myData.to_csv (r'/Users/trangvu/Desktop/syllabi/features-retrieved-by-trangvu.csv', index = None)


# ***In overall I have extracted Phone, Email, Professor Name, Website, Prequisite, Location, Office Hour, Textbook, Homework,Final,Course Description and Course Policy.***
