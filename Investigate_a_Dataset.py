#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset - [No-show appointments!]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row.
# 
# 
# ### Question(s) for Analysis
# How did the attendence has been affected by the effects mentioned in Columns ?

# In[3]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# In[ ]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you **document your data cleaning steps in mark-down cells precisely and justify your cleaning decisions.**
# 
# 
# ### General Properties
# 

# In[4]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df= pd.read_csv('noshowappointments-kagglev2-may-2016.csv')
df.head()


# In[5]:


#Chceking for data Shape
df.shape


# Data include 14 column and 110527 column
# 

# In[6]:


df.describe()


# data include unreal age -1 so it is an error will be dropped
# 
# 

# In[7]:


age_negative = df.query('Age < 0')
age_negative


# only one row is -1 and will be dropped
# 
# 

# In[8]:


df.isnull().sum()


# there is no any NaN values

# In[9]:


df.info()


# In[10]:


df.duplicated().sum()


# there is no duplicated rows

# In[11]:


df.nunique()


# - all the appointments will be done within 27 days
# - only 62299 from 110527 so the Patient ID will be checked for dupplicates as may be some patients get more than 1 appointment
# - Patients will be come from 81 places

# In[12]:


#ScheduledDay is an object and will be changed to date
sch_day = ['ScheduledDay']
for x in sch_day:
    df[x] = pd.to_datetime(pd.to_datetime(df[x]).dt.date)


# In[13]:


last_day = df['ScheduledDay'].max()
last_day


# In[14]:


first_day = df['ScheduledDay'].min()
first_day


# In[15]:


schedualed_period = last_day - first_day
schedualed_period


# all apointments schedualed to be done within 211 days from 2015-11-10 to 2016-06-08

# In[16]:


#ScheduledDay is an object and will be changed to date
app_day = ['AppointmentDay']
for x in app_day:
    df[x] = pd.to_datetime(pd.to_datetime(df[x]).dt.date)


# In[17]:


first_app_day = df['AppointmentDay'].min()
first_app_day


# In[18]:


last_app_day = df['AppointmentDay'].max()
last_app_day


# In[19]:


actual_period = last_app_day - first_app_day
actual_period


# the appointments done within 40 days, so may be some of patients attended in different times

# In[20]:


df['PatientId'].duplicated().sum()


# duplicated Patient ID will be dropped

# In[ ]:





# 
# ### Data Cleaning
# I changed no-show to no_show and also dropped al the dupplicated patients and the unreal age values  

# In[21]:


#changing the column name from 'No-show' to 'No_show'
df.rename(columns = {'No-show' : 'No_show'}, inplace = True)
df.head()


# In[22]:


# drop the dupplicated patients with the same no_show status 
df.drop_duplicates(['PatientId', 'No_show'], inplace = True)


# In[23]:


df.shape


# In[24]:


# drop the age_negative
df.drop(age_negative.index, inplace = True)


# In[25]:


df.shape


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# I created a chart for every item to check its effect on the attendence 
# 
# 
# 

# In[26]:


df.hist(figsize = (20,7));


# In[27]:


# Distrbuting of patients who is attended and not_attended 
attended = df.No_show == 'No'
absent = df.No_show == 'Yes'


# In[28]:


attended.sum()


# In[29]:


absent.sum()


# 54153 as been attended and 17663 has not been attended

# In[30]:


df[attended][('Age')].mean()


# In[31]:


df[absent][('Age')].mean()


# The attended and abset Patients are almost the same age average

# In[32]:


df[attended][('SMS_received')].mean()


# In[33]:


df[absent][('SMS_received')].mean()


# almost 30% who they attended received SMS and 45% of the Absent so may be the SMS is not enough clear for the Patients

# In[34]:


df[absent][('Hipertension')].mean()


# In[35]:


df[attended][('Hipertension')].mean()


# In[36]:


df[attended][('Diabetes')].mean()


# In[37]:


df[absent][('Diabetes')].mean()


# Hipertension & Diabetes didn't affect the attendence of Patients 

# # Research Question 1 (Age effect on the attendence !)

# In[ ]:





# In[55]:


def attendence_bar (df,column, attended, absent, title,xlabel,ylabel):
    plt.figure(figsize=(20,4))
    df[column][attended].value_counts().plot(kind='bar', color='green', label = 'Attended')
    df[column][absent].value_counts().plot(kind='bar', color='red', label = 'Absent')
    plt.title(title)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel);
attendence_bar(df,'Age', attended, absent,'Age effect on the attendence', 'Age', 'Patient ID' )


# Most of attended patient are young so the age affect on attendence 

# ### Research Question 2  (Neighbourhood effect on the attendence)

# In[56]:


attendence_bar(df,'Neighbourhood', attended, absent,'Neighbourhood effect on the attendence', 'Neighbourhood', 'Patient ID' )


# Most of attended patient are from Jardim Camburi so I think this is the nearest place to the attendence location

# # Research Question 3  (Gender effect on the attendence)

# In[57]:


plt.figure(figsize=(10,5))
df.Gender[attended].value_counts().plot(kind='pie')
df.Gender[absent].value_counts().plot(kind='pie')
plt.title('Gender effect on the attendence')

plt.xlabel('Gender')
plt.ylabel('Patient ID');


# # # Research Question 4  (Hipertension effect on the attendence)

# In[58]:


attendence_bar(df,'Hipertension', attended, absent,'Hipertension effect on the attendence', 'Hipertension', 'Patient ID' )


# Most of  patient infected with Hipertension attended so it didn't affect the attendence

# # # Research Question 5  (Scholarship effect on the attendence)

# In[59]:


attendence_bar(df,'Scholarship', attended, absent,'Scholarship effect on the attendence', 'Scholarship', 'Patient ID' )


# Scholarship has not affected the attendence 

# # # Research Question 6  (SMS_received effect on the attendence)

# In[60]:


attendence_bar(df,'SMS_received', attended, absent,'SMS_received effect on the attendence', 'SMS_received', 'Patient ID' )


# Most of attended Patients didn't receive SMS and almost 50% of receiving SMS have been attended so the SMS didn't affect the attendence 

# # # Research Question 7  (Diabetes effect on the attendence)

# In[61]:


attendence_bar(df,'Diabetes', attended, absent,'Diabetes effect on the attendence', 'Diabetes', 'Patient ID' )


# Most of patients are not infected with Diabetes however most of infected patients attended so Diabetes didn't affect the attendence 

# <a id='conclusions'></a>
# ## Conclusions
# The Attendence only was affected with the Age and the Locations of Patients and the remaining effects haven't affected 
# 
# ## Submitting your Project 
# 
# 

# In[88]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




