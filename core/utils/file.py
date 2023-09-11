import os
import glob
import traceback
from shutil import make_archive
from utils.log import Logger
from datetime import date

MEDIA = "/core/media/"
FINAL_REPORT = os.getenv("FINAL_REPORT")
WAREHOUSE_REPORT = os.getenv("WAREHOUSE_REPORT")

class File():
    
    def __init__(self, logger: Logger):
        self.logger = logger 
        self.zip_file = f'{WAREHOUSE_REPORT}BGT_Checklist_{str(date.today().strftime("%d/%m/%Y")).replace("/","_")}'
    
    def conpress_zip_file(self):
        try:
            make_archive(self.zip_file, 'zip', root_dir=FINAL_REPORT)
            return f"{self.zip_file}.zip"
        except Exception as error:
            self.logger.log_message(error, "error")
            traceback.print_exception()
            return 
        
    def clear_old_file(self) -> None:
        try:
            files = glob.glob(f'{WAREHOUSE_REPORT}*') + glob.glob(f'{FINAL_REPORT}*')
            for f in files:
                os.remove(f)
        except Exception as error:
            traceback.print_exception()
            self.logger.log_message(error, "error")