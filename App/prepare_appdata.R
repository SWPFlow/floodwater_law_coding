
# run this locally before uploading, if new Files are added

# ===== fuck encoding - run this before redeploying if new files are added =====
for (file in seq_along(filelist)) {
  imported_file <- read.csv(paste("./original_data",
                                  filelist[file], sep = "/"),
                            sep = ";", stringsAsFactors = F,
                            encoding = "ANSI")
  # imported_file <- import
  write.csv2(imported_file,file = paste("./appdata",filelist[file], sep = "/"),
             fileEncoding = "UTF-8")
}
