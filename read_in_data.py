
import os

path_to_htmlfiles = os.getcwd() + "\\Data" #get path to where csv are stored

html_list = os.listdir(path_to_htmlfiles) #list all the html that are in the folder

filepath_list = [path_to_htmlfiles + "\\" + html_file for html_file in html_list] #get list of filepaths


from bs4 import BeautifulSoup

with open(filepath_list[0], encoding = "UTF-8") as fp:
    soup = BeautifulSoup(fp) #make soup object

print(soup) #look at it

soup.title.string #get law title

soup.find_all("h5") #get all tags containing article headers

# print article numbers and titles

for article in soup.find_all("h5"):
    for article_name_tag in article.find_all("a"):
        for text_element in article_name_tag:
            print(text_element.string)
  
#for article in soup.find_all("h5"):
#    print(article.get_text())      
    
soup.find_all("div", {"class": "collapseableArticle"}) #get all tags containing article texts


for article_text in soup.find_all("div", {"class": "collapseableArticle"}):
    for p_text in article_text.find_all("p"):
        print(p_text.get_text())
    
