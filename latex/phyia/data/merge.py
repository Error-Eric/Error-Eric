import os
import re
import xlrd
import xlwt
from xlrd import XL_CELL_ERROR

def merge_xls_files(file_list, output_filename="data.xls"):
    out_wb = xlwt.Workbook()
    used_sheet_names = set()
    
    for file_path in file_list:
        try:
            in_wb = xlrd.open_workbook(file_path)
            in_sheet = in_wb.sheet_by_index(0)
            
            base_name = os.path.basename(file_path)
            clean_name = re.sub(r'[\\/*\[\]:?]', '', base_name)
            if len(clean_name) > 31:
                clean_name = clean_name[:31]
            
            candidate = clean_name
            counter = 1
            while candidate in used_sheet_names:
                suffix = f"({counter})"
                base_length = 31 - len(suffix)
                base_part = clean_name[:base_length] if len(clean_name) > base_length else clean_name
                candidate = base_part + suffix
                counter += 1
            
            sheet_name = candidate
            used_sheet_names.add(sheet_name)
            out_sheet = out_wb.add_sheet(sheet_name)
            
            for row_idx in range(in_sheet.nrows):
                for col_idx in range(in_sheet.ncols):
                    cell = in_sheet.cell(row_idx, col_idx)
                    if cell.ctype == XL_CELL_ERROR:
                        out_sheet.write(row_idx, col_idx, '#ERROR!')
                    else:
                        out_sheet.write(row_idx, col_idx, cell.value)
        except: pass
    
    out_wb.save(output_filename)

if __name__ == "__main__":
    filelist = []
    for r in [2.5 + i for i in range(7)]:
        for t in range(1,7):
            filelist.append(f"R={r}({t}).xls")
    merge_xls_files(file_list= filelist)
    