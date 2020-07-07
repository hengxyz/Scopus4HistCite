# coding:utf-8
import os
import time

def Scopus2HistCite():
    try:
        #files = glob.glob('woc.txt')


        file = 'wos1.txt'
        if os.path.isfile(file):

            Scopus_file = file
            # print('Delete the generated files!')
            # os.system('del *.dbf')
            # os.system('del *.dbt')
            # os.system('del *.ntx')
            # #os.system('move wos.txt ..\wos.txt') ##windows is \
            # os.system('del temp.txt')
            # os.system('del abstract.txt')
            # os.system('del scopus.txt')
            # #os.system('move ..\wos.txt wos.txt')
            # #time.sleep(10)
            # print("You are going to transforming the Scopus format to WOS format!")
            # strcmd = 'PowerShell -Command "& {get-content wos.txt -encoding utf8 | set-content wos1.txt -encoding utf8}"'
            # os.system(strcmd) ## change the wos.txt as utf-8 format
            # time.sleep(1)
            # os.system('del wos.txt')
            # os.system('move wos1.txt wos.txt')
        else:
            raise Exception("No file spcified")

        CR_block = False
        dict_ref = {}
        i = 0
        Lines = []
        with open(Scopus_file, 'r') as Scopus:
            for line in Scopus.readlines():
                # if line == 'TI Face spoof detection with image distortion analysis\n':
                #     print('stop')
                if line[:2] == 'AU':
                    line = line.upper()
                    author = line[3:-1]
                    author = author.replace(',', '')
                if line[:2] == 'PY':
                    year = line[3:-1]
                if line[:2] == 'SO':
                    so = line[3:-1]
                if line[:2] == 'J9':
                    j9 = line[3:-1]
                if line[:2] == 'TI':
                    ti = line[3:-1]
                if line[:2] == 'VL':
                    VL = line[3:-1]
                    if  VL == '':
                        VL='11'
                        line = line[:-1]+' '+VL+'\n'
                if line[:2] == 'BP':
                    BP = line[3:-1]
                    if not BP:
                        BP='11'
                        line = line[:-1] + ' ' + BP + '\n'
                    dict_ref['%d'%i] = [author, year, so, VL, BP, j9, ti]
                    i += 1
                Lines.append(line)

        with open(Scopus_file, 'w') as Scopus:
            Scopus.writelines(Lines)

        Lines = []
        with open(Scopus_file, 'r') as Scopus:
            for line in Scopus.readlines():
                # if line == 'TI Spoofing in 2D face recognition with 3D masks and anti-spoofing with Kinect\n':
                #     print('stop')

                if line[:2] == 'CR':
                    CR_block = True
                    line = line[:-1]
                    line = line.upper()
                    strs = line.split(',')
                    author = strs[0][3:]
                    author = author.upper()
                    year = strs[1][1:]
                    so = strs[2][1:]
                    so = so.upper()
                    # if author == 'CHINGOVSKA I' and year == '2012':
                    #     print('stop')


                    #idx = [i for i, value in enumerate(list(dict_ref.values())) if author==value[0] and year==value[1] and ti==value[2]]
                    #idx = [i for i, value in enumerate(list(dict_ref.values())) if author==value[0].upper() and year==value[1] and (ref[2].upper() in so or ref[5].upper() in so)]
                    #idx = [i for i, value in enumerate(list(dict_ref.values())) if author==value[0].upper() and year==value[1]]
                    idx = [i for i, value in enumerate(list(dict_ref.values())) if author==value[0].upper() and year==value[1]]
                    if idx and len(author):
                        if len(idx) == 1:
                            ref = dict_ref['%d' % (idx[0])]
                            VL = ref[3]
                            BP = ref[4]
                            line = strs[0]+',' + strs[1]+',' + strs[2]+',' + 'V' + VL + ', P' + BP + strs[5]+'\n'
                        else:
                            goodref = False
                            for i in idx:
                                ref = dict_ref['%d' % (i)]
                                if author == ref[0].upper() and year == ref[1] and so == ref[2].upper():
                                    VL = ref[3]
                                    BP = ref[4]
                                    goodref = True
                                    break
                            if not goodref:
                                ref = dict_ref['%d' % (0)]
                                VL = ref[3]
                                BP = ref[4]
                            line = strs[0] + ',' + strs[1] + ',' + strs[2] + ',' + 'V' + VL + ', P' + BP + strs[5]+'\n'

                    else:
                        line += '\n'

                else:
                    if line[:2] == "NR":
                        CR_block = False

                    if CR_block:
                        line = line[:-1]
                        line = line.upper()
                        strs = line.split(',')
                        author = strs[0][1:]
                        author = author.upper()
                        year = strs[1][1:]
                        so = strs[2][1:]
                        so = so.upper()
                        if author == 'CHINGOVSKA I' and year == '2012':
                            print('stop')

                        idx = [i for i, value in enumerate(list(dict_ref.values())) if author == value[0].upper() and year == value[1]]
                        if idx and len(author):
                            if len(idx) == 1:
                                ref = dict_ref['%d' % (idx[0])]
                                VL = ref[3]
                                BP = ref[4]
                                line = strs[0] + ',' + strs[1] + ',' + strs[2] + ',' + ' V' + VL + ', P' + BP + strs[5]+'\n'
                            else:
                                goodref = False
                                for i in idx:
                                    ref = dict_ref['%d' % (i)]
                                    if author == ref[0].upper() and year == ref[1] and so == ref[2].upper():
                                        VL = ref[3]
                                        BP = ref[4]
                                        goodref = True
                                        break
                                if not goodref:
                                    ref = dict_ref['%d' % (0)]
                                    VL = ref[3]
                                    BP = ref[4]
                                line = strs[0] + ',' + strs[1] + ',' + strs[2] + ',' + ' V' + VL + ', P' + BP + strs[5] +'\n'
                        else:
                            line += '\n'
                Lines.append(line)

        with open('wos2.txt', 'w') as Scopus:
            Scopus.writelines(Lines)


    except Exception as e:
        raise e


if __name__ == '__main__':
    Scopus2HistCite()