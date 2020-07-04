# coding:utf-8
import os
import time

def Scopus2HistCite():
    try:
        #files = glob.glob('woc.txt')


        file = 'wos.txt'
        if os.path.isfile(file):
            print('Delete the generated files!')
            os.system('del *.dbf')
            os.system('del *.dbt')
            os.system('del *.ntx')
            #os.system('move wos.txt ..\wos.txt') ##windows is \
            os.system('del temp.txt')
            os.system('del abstract.txt')
            os.system('del scopus.txt')
            #os.system('move ..\wos.txt wos.txt')
            #time.sleep(10)
            print("You are going to transforming the Scopus format to WOS format!")
            Scopus_file = file
            strcmd = 'PowerShell -Command "& {get-content wos.txt -encoding utf8 | set-content wos1.txt -encoding utf8}"'
            os.system(strcmd) ## change the wos.txt as utf-8 format
            time.sleep(1)
            os.system('del wos.txt')
            os.system('move wos1.txt wos.txt')
        else:
            raise Exception("No file spcified")

        CR_block = False
        dict_ref = {}
        i = 0
        Lines = []
        with open(Scopus_file, 'r') as Scopus:
            for line in Scopus.readlines():
                if line[:2] == 'AU':
                    line = line.upper()
                    author = line[3:-1]
                    author = author.replace(',', '')
                if line[:2] == 'PY':
                    year = line[3:-1]
                if line[:2] == 'VL':
                    VL = line[3:-1]
                    if not VL:
                        VL='0'
                        line = line[:-1]+VL+'\n'
                if line[:2] == 'BP':
                    BP = line[3:-1]
                    if not BP:
                        BP='0'
                        line = line[:-1] + BP + '\n'
                    dict_ref['%d'%i] = [author, year, VL, BP]
                    i += 1
                Lines.append(line)

        with open(Scopus_file, 'w') as Scopus:
            Scopus.writelines(Lines)

        Lines = []
        with open(Scopus_file, 'r') as Scopus:
            for line in Scopus.readlines():
                if line[:2] == 'CR':
                    CR_block = True
                    line = line[:-1]
                    line = line.upper()
                    strs = line.split(',')
                    author = strs[0][3:]
                    year = strs[1][1:]

                    idx = [i for i, value in enumerate(list(dict_ref.values())) if author in value and year in value]
                    if idx:
                        ref = dict_ref['%d' % (idx[0])]
                        VL = ref[2]
                        BP = ref[3]
                        line = strs[0]+', ' + strs[1]+', ' + strs[2]+', ' + 'V' + VL + ', P' + BP + '\n'
                    else:
                        line += '\n'

                else:
                    if line[:2] == "NR":
                        CR_block = False

                    if CR_block:
                        line = line[:-1]
                        line = line.upper()
                        strs = line.split(',')
                        author = strs[0][3:]
                        year = strs[1][1:]


                        idx = [i for i, value in enumerate(list(dict_ref.values())) if author in value and year in value]
                        if idx:
                            ref = dict_ref['%d'%(idx[0])]
                            VL = ref[2]
                            BP = ref[3]
                            line = strs[0]+', ' + strs[1]+', ' + strs[2]+', ' + 'V' + VL + ', P' + BP+'\n'
                        else:
                            line += '\n'

                Lines.append(line)

        with open(Scopus_file, 'w') as Scopus:
            Scopus.writelines(Lines)


    except Exception as e:
        raise e


if __name__ == '__main__':
    Scopus2HistCite()