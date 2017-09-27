
import os
import csv

path_to_htmlfiles = os.getcwd() + "\\Data" #get path to where csv are stored

html_list = os.listdir(path_to_htmlfiles) #list all the html that are in the folder

filepath_list = [path_to_htmlfiles + "\\" + html_file for html_file in html_list] #get list of filepaths


from bs4 import BeautifulSoup

# ========== example read in third law and print cleanly to console ============

with open(filepath_list[2], encoding = "UTF-8") as fp:
    soup = BeautifulSoup(fp) #make soup object

print(soup) #look at it

soup.title.string #get law title


           
for lawcontent in soup.find_all("div", {"id": "lawcontent"}):
    for children in lawcontent.find_all(recursive = True): #recursive = False to only get the next level children
        if children.name == "h5": #h5 tags are around article headers
            print(children.strong.string)
            print(children.get_text())
            if children.nextSibling.attrs['class'] != ['collapseableArticle']: #make sure after the article header comes law text
                print("***** \n no article text after article title")
                break
            paragraphs_list = [paragraph.get_text() for paragraph in children.nextSibling.find_all("p")]
            print("\n".join(paragraphs_list))

                

# =========== define function to write soup object into dict =================       

def write_soup_law_to_articles_list(soup_object):

    law_list = []
    
    for lawcontent in soup_object.find_all("div", {"id": "lawcontent"}):
        for children in lawcontent.find_all(recursive = True): #recursive = False to only get the next level children
            if children.name == "h5": #h5 tags are around article headers
                if children.nextSibling.attrs['class'] != ['collapseableArticle']: #make sure after the article header comes law text
                    print("\n ***** no article text after article title")
                    break
                paragraphs_list = [paragraph.get_text() for paragraph in children.nextSibling.find_all("p")]
                article_list_entry = {'article_number': children.strong.string,
                                  'article_title': children.get_text(),
                                  'article_text': "\n".join(paragraphs_list)}
                law_list.append(article_list_entry)
                
    return(law_list)

#test_law_list = write_soup_law_to_articles_list(soup)
#print(test_law_list[5]['article_text'])

# ============= function to write to csv ===============



def write_articles_list_to_csv(article_list):
    
    keys = article_list[0].keys()
    with open(os.getcwd() + "\\Initial law processing output" + '\\{}.csv'.format(soup.title.string), 'w', encoding = "UTF-8", 
              newline = '') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(article_list)
        

# ============ write all laws into files ==========

for file in filepath_list:
    with open(file, encoding = "UTF-8") as fp:
        soup = BeautifulSoup(fp) #make soup object  
    list_of_articles = write_soup_law_to_articles_list(soup)
    write_articles_list_to_csv(list_of_articles)
    
