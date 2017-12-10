
library("shiny")
library("statnet")
library("GGally")
library("tidyr")

## DATA DESCRIPTION
# We (Andrea Ghisletta) coded all Swiss national-level laws, and laws of the Canton of Bern
# which relate to flood protection.
# He coded different types of "issues" addressed in the laws that address flood protection. 
# see codebook with issues, domains, projects (=different levels of abstraction of issues)

#==================================================================================
## DATA ###
#==================================================================================
## IMPORT DATA

filelist <- list.files("./appdata", pattern = ".csv")
lawfile_list <- as.list(rep(NA,length(filelist)))

for (file in seq_along(filelist)) {
  imported_file <- read.csv(paste("./appdata",
                                  filelist[file], sep = "/"), 
                            sep = ";", stringsAsFactors = F,
                            encoding = "UTF-8", strip.white = T)
  imported_file <- imported_file[,colnames(imported_file) != "X"]
  assign(sub(filelist[file], pattern = ".csv", replacement = ""), imported_file)
  lawfile_list[[file]] <- get(sub(filelist[file], pattern = ".csv", replacement = ""))
}

#==================================================================================
## EDGELISTS ##
#==================================================================================

#### ------- create edgelists for all legal texts ------ ####

prepare_el <- function(law_file, law_name){
  law_file <- law_file[-c(2,3,4)] # remove all unneccessary variables
  law_file[law_file == ""] <- NA # empty cells as NA
  law_file[law_file == "NA"] <- NA
  law_file[is.na(law_file)] <- NA
  law_file$law <- paste(rep(law_name,nrow(law_file)),law_file$article_number)
  str_mat <- apply(law_file[,c(3:ncol(law_file) - 1) ], 1, paste)
  colnames(str_mat) <- law_file$law
  namevec <- unlist(lapply(law_file$law,FUN = rep, nrow(str_mat)))
  issuevec <- c(str_mat)
  law_file_el <- cbind(namevec, issuevec)
  law_file_el <- law_file_el[law_file_el[,2] != "NA",]
  return(law_file_el)
}

for (object in c(1:length(lawfile_list))){
  name <- paste(sub(filelist[object], pattern = ".csv", replacement = ""),"_el", sep = "")
  assign(name, prepare_el(lawfile_list[[object]], name)) 
}

#### ----- bind all edgelists into one edgelist --------

el <- rbind(AuenV_el, BV_el, BZG_el, GSchG_el, GSchV_el, NHG_el, NHV_el, RPG_el, RPV_el, StAG_el, StAV_el, VNAZ_el, VWAS_el, WaG_el, WaV_el, WBG_el, WBV_el) 
el <- as.data.frame(el)
colnames(el) <- c("article","issue")

## --- create a list of law names -------

lawname_list <- unlist(lapply(filelist, sub, pattern = ".csv", replacement = ""))
lawname_list <- lawname_list[lawname_list != c("issuelist")]

