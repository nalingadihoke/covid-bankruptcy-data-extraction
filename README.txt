-- install shutil
-- install selenium
-- install requests
-- install any other packages
-- python 3 needed

1. 

.... $ cd *change to directory containing code files*

2. 

Terminal input format:

.... $ python scrape_scrape.py full_input_file_path full_output_folder_path chromedriver_path


Notes:

-- This script will download the top four bankruptcy data ranked by number of entries. These generally are Chapter 11, 7, 13 and 12.

-- Script may crash on rare occasion due to buffer speeds and inconsistencies in the website (it is not optimised for easy scraping).

-- Do not close terminal or interrupt process while script is running, even if the browser closes temporarily.