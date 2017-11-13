
import os
import csv

path_to_htmlfiles = os.getcwd() + "\\Data Bern" #get path to where csv are stored

html_list = os.listdir(path_to_htmlfiles) #list all the html that are in the folder

filepath_list = [path_to_htmlfiles + "\\" + html_file for html_file in html_list] #get list of filepaths


from bs4 import BeautifulSoup

# ========== example read in first law and print cleanly to console ============

with open(filepath_list[0], encoding = "UTF-8") as fp:
    soup = BeautifulSoup(fp) #make soup object

print(soup) #look at it

soup.title.string #get law title
          
for section in soup.findAll("div", {"class": "article"}):
    print(section.get_text())
    print("".join([div.get_text() for div in section.find_all(True, {"class": "number"})]))
    nextNode = section
    while True:
        nextNode = nextNode.find_next_sibling()
        next_class_name = nextNode.get("class")
        if next_class_name != ["article"]:
            if next_class_name == ["paragraph"]:
                print(nextNode.get_text())
            if next_class_name == ["enumeration_item"]:
                print(nextNode.get_text())
            else:
                pass
        if next_class_name == ["article"] or next_class_name == ["egress_sign_off_date"]:
            print("**************")
            break

                

# =========== define function to write soup object into dict =================       

def write_soup_law_to_articles_list(soup_object):

    law_list = []
    
    for section in soup.findAll("div", {"class": "article"}):
        title = section.get_text()
        article_number = "".join([div.get_text() for div in section.find_all(True, {"class": "number"})])
        paragraphs_list = []
        nextNode = section       
        while True:
            nextNode = nextNode.find_next_sibling()
            next_class_name = nextNode.get("class")
            
            if next_class_name != ["article"]:
                if next_class_name == ["paragraph"]:
                    paragraphs_list.append(nextNode.get_text())
                if next_class_name == ["enumeration_item"]:
                    paragraphs_list.append(nextNode.get_text())
                else:
                    pass
            if next_class_name == ["article"] or next_class_name == ["egress_sign_off_date"]:
                article_list_entry = {'article_number': article_number,
                                          'article_title': title,
                                          'article_text': "\n".join(paragraphs_list)}
                law_list.append(article_list_entry)
                break        
    return(law_list)
                

#test_law_list = write_soup_law_to_articles_list(soup)
#print(test_law_list[5]['article_text'])

# ============= function to write to csv ===============



def write_articles_list_to_csv(article_list):
    
    keys = article_list[0].keys()
    with open(os.getcwd() + "\\Initial law processing output Bern" + '\\{}.csv'.format(soup.title.string), 'w', encoding = "UTF-8", 
              newline = '') as f:
        dict_writer = csv.DictWriter(f, keys, delimiter = ';', dialect = 'excel')
        dict_writer.writeheader()
        dict_writer.writerows(article_list)
        

# ============ write all laws into files ==========

#for file in filepath_list:
#    with open(file, encoding = "UTF-8") as fp:
#        soup = BeautifulSoup(fp) #make soup object  
#    list_of_articles = write_soup_law_to_articles_list(soup)
#    write_articles_list_to_csv(list_of_articles)
 
# =========== write with different encoding ===========
    
for file in filepath_list:
    with open(file, encoding = "UTF-8") as fp:
        soup = BeautifulSoup(fp) #make soup object  
    list_of_articles = write_soup_law_to_articles_list(soup)
    write_articles_list_to_csv(list_of_articles)
 

# =========== write all csvs to xlsx files :( =================

                                             
 # write list csv filenames
 
#path_to_csvfiles = os.getcwd() + "\\Initial law processing output" #get path to where csv are stored
#
#csv_list = os.listdir(path_to_csvfiles) #list all the html that are in the folder
#
#csv_filepath_list = [path_to_csvfiles + "\\" + csv_file for csv_file in csv_list] #get list of filepaths
#
# 
#                                             
#import glob
#import csv
#import xlwt # from http://www.python-excel.org/
#
#for csvfile in csv_filepath_list:
#    wb = xlwt.Workbook()
#    ws = wb.add_sheet('data')
#    with open(csvfile, 'rb') as f:
#        reader = csv.reader(f)
#        for r, row in enumerate(reader):
#            for c, val in enumerate(row):
#                ws.write(r, c, val)
#    wb.save(csvfile + '.xls')