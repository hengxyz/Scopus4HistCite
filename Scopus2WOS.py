# coding:utf-8
import os
import re
#import time

def Scopus2HistCite():
    try:
        #files = glob.glob('woc.txt')

        Scopus_file = 'scopus_972.ris'

        if not os.path.isfile(Scopus_file):
            raise Exception("No file spcified")



        Lines_wos = []
        line_wos = "FN Thomson Reuters Web of Knowledge™\n"
        Lines_wos.append(line_wos)
        line_wos = "VR 1.0\n"
        Lines_wos.append(line_wos)
        Lines_wos.append('\n')


        CR_block = False
        dict_ref = {}
        i = 0
        Lines_section = []
        read_section = False
        process = False
        with open(Scopus_file, 'r') as Scopus:
            for line in Scopus.readlines():
                if line[:2] == 'TY':
                    read_section = True
                if line[:2] == 'ER':
                    read_section = False
                    process = False
                if read_section:
                    Lines_section.append(line)
                else:
                    if process == True:
                        continue
                    ## transforming the scopus to wos format:
                    Lines_wos.append('PT J\n')
                    ## TY
                    lines_TY = [line for line in Lines_section if 'TY ' in line]
                    doctype = lines_TY[0][6:-1]

                    ## AU
                    lines_AU = [line for line in Lines_section if 'AU ' in line]
                    if lines_AU:
                        name = lines_AU[0][6:]
                        name = name.replace('.', '')
                        if ',' in name:
                            strs_name = name.split(',')
                            name0 = strs_name[0]
                            if ' ' in name0:
                                name0 = name0.replace(' ','')
                                name = name0+','+strs_name[1]
                        else:
                            print('%s'%name)
                        Lines_wos.append('AU %s'%name)
                        for line in lines_AU[1:]:
                            line = line.replace('.', '')
                            Lines_wos.append(' %s'%line[6:])
                    else:
                        lines_AU = [line for line in Lines_section if 'A2 ' in line]
                        if lines_AU:
                            name = lines_AU[0][6:]
                            name = name.replace('.', '')
                            if ',' in name:
                                strs_name = name.split(',')
                                name0 = strs_name[0]
                                if ' ' in name0:
                                    name0 = name0.replace(' ', '')
                                    name = name0 + ',' + strs_name[1]
                            else:
                                print('%s' % name)
                            Lines_wos.append('AU %s'%name)
                            for line in lines_AU[1:]:
                                line = line.replace('.', '')
                                Lines_wos.append(' %s'%line[6:])
                        else:
                            Lines_wos.append('AU\n')


                    ## TI
                    lines_TI = [line for line in Lines_section if 'TI ' in line]
                    Lines_wos.append('TI %s' % lines_TI[0][6:])
                    if lines_TI[0][6:] == 'Non-intrusive liveness detection by face images\n':
                        print('stop')
                    ## SO
                    if doctype == 'JOUR' or doctype == 'CHAP':
                        lines_T2 = [line for line in Lines_section if 'T2 ' in line]
                        Lines_wos.append('SO %s' % lines_T2[0][6:])
                    else:
                        lines_T2 = [line for line in Lines_section if 'C3 ' in line]
                        if lines_T2:
                            Lines_wos.append('SO %s' % lines_T2[0][6:])
                        else:
                            lines_T2 = [line for line in Lines_section if 'T2 ' in line]
                            if lines_T2:
                                Lines_wos.append('SO %s' % lines_T2[0][6:])
                            else:
                                Lines_wos.append('SO\n')

                    ## LA
                    lines_LA = [line for line in Lines_section if 'LA ' in line]
                    Lines_wos.append('LA %s' % lines_LA[0][6:])

                    ## DT
                    lines_DT = [line for line in Lines_section if 'TY ' in line]
                    Lines_wos.append('DT %s' % lines_DT[0][6:])

                    ## DE %KEYWORDS
                    lines_KW = [line for line in Lines_section if 'KW ' in line]
                    strkw = 'DE'
                    for line in lines_KW:
                        strkw += ' %s;'%line[6:-1]
                    Lines_wos.append('%s\n'%strkw)

                    ## AB
                    lines_AB = [line for line in Lines_section if 'AB ' in line]
                    if lines_AB:
                        Lines_wos.append('AB %s' % lines_AB[0][6:])
                    else:
                        Lines_wos.append('AB\n')

                    ## C1 %Affliation
                    if 'AD' in line:
                        lines_C1 = [line for line in Lines_section if 'AD ' in line]
                        Lines_wos.append('C1 %s'%lines_C1[0][6:])
                        for line in lines_C1[1:]:
                            Lines_wos.append(' %s'%line[6:])
                    else:
                        Lines_wos.append('C1\n')

                    ## RP
                    Lines_wos.append('RP\n')

                    ## CR %Reference
                    idx_CR = 0
                    lines_CR = []
                    for i, line in enumerate(Lines_section):
                        if 'References' in line:
                            idx_CR = i
                            lines_CR.append(line[18:])
                            break
                    for line in Lines_section[idx_CR+1:]:
                        if 'UR ' in line and line.index('UR ')>2:
                            line = line[:line.index('UR ')]+'\n'
                        if line[:2] == 'UR':
                            break
                        if ';' in line:
                            if line.index(';') < len(line)-5:
                                idxs = [i for i, c in enumerate(line) if c==';']
                                begin = 0
                                for i in range(len(idxs)):
                                    line_temp=line[begin:idxs[i]+1]+'\n'
                                    lines_CR.append(line_temp)
                                    begin = idxs[i]+2
                                if idxs[i] < len(line)-5:
                                    line_temp = line[idxs[i]+2:]
                                    lines_CR.append(line_temp)
                                continue

                        lines_CR.append(line)

                    lines_CR_wos = []
                    for line in lines_CR:
                        ## name
                        if '.,' in line:
                            name = line[:line.index('.,')]
                            name = name.replace(',', '')
                        else:
                            name = ''
                        ## year
                        match = re.match(r'.*(\([1-3][0-9]{3}\))', line)
                        if match is None:
                            match = re.match(r'.*([1-3][0-9]{3}\,)', line)
                            if match is None:
                                year = ''
                            else:
                                year = match.group(1)
                                year = year[:-1]
                        else:
                            year = match.group(1)
                            year = year[1:-1]
                        #year = line[line.index('(')+1:line.index(')')]
                        ## conf/journal name
                        idx_docname = line.index('%s'%year)
                        if idx_docname:
                            if ',' in line[idx_docname + 6:]:
                                idx = line[idx_docname + 6:].index(',')
                                docname = line[idx_docname + 6:idx_docname + 7 + idx]
                            else:
                                if 'Proc' in line:
                                    idx_proc = line.index('Proc')
                                    docname = line[idx_proc + 5:line.index(year)-2]
                                else:
                                    if ';' in line[idx_docname + 6:]:
                                        idx = line[idx_docname + 6:].index(';')
                                        docname = line[idx_docname + 6:idx_docname + 6+idx]
                                    else:
                                        docname = ''
                        if docname:
                            docname = docname.replace(',', '')
                        ## volumen
                        line_volume = line[line.index(year)+5:]
                        if '(' in line_volume:
                            if ',' in line_volume:
                                volume = line_volume[line_volume.index(','):line_volume.index('(')-1]
                            else:
                                volume = ''
                            if volume:
                                r1 = re.findall(r"\d{1,3}", volume)
                                #match = re.match(r'.*([0-9]{0,3})', volume)
                                if r1:
                                    volume = r1[0]
                                else:
                                    volume = ''
                            else:
                                volume = ''
                        else:
                            volume = ''
                        ## page number
                        if 'pp.' in line:
                            idx_page = line.index('pp.')
                            if '-' in line[idx_page+3:]:
                                page = line[idx_page+3:idx_page+3+line[idx_page+3:].index('-')]
                            else:
                                page = ''
                        else:
                            if 'p.' in line:
                                idx_page = line.index('p.')
                                if '-' in line[idx_page+2:]:
                                    page = line[idx_page+2:idx_page+2+line[idx_page+2:].index('-')]
                                elif '.' in line[idx_page + 2:]:
                                    page = line[idx_page + 3:idx_page + 2 + line[idx_page + 2:].index('.')]
                                elif ';' in line[idx_page + 2:]:
                                    page = line[idx_page + 3:idx_page + 2 + line[idx_page + 2:].index(';')]
                                else:
                                    page = ''
                            else:
                                page = ''

                        ## TI, title of paper
                        if '.,' in line:
                            idx_ti = len(line)-line[::-1].index(',.')-1
                        else:
                            ti = docname
                        idx_docname = line.index('%s' % year)
                        if idx_docname:
                            ti = line[idx_ti+1:idx_docname-1]
                            if ti == ' ' :
                                line_ti = line[idx_docname+5:]
                                if ',' in line_ti:
                                    ti = line_ti[: line_ti.index(',')]
                                else:
                                    ti = ''
                        else:
                            line_ti = line[idx_ti+1:]
                            if ',' in line_ti:
                                ti = line_ti[1: line_ti.index(',')]
                            else:
                                ti = ''


                        lines_CR_wos.append([name, year, docname, volume, page, ti])

                    lines_CR_wos[0][3] = lines_CR_wos[0][3].replace(' ', '')
                    lines_CR_wos[0][4] = lines_CR_wos[0][4].replace(' ', '')
                    Lines_wos.append('CR %s, %s, %s, V%s, P%s, %s\n'%(lines_CR_wos[0][0],lines_CR_wos[0][1],lines_CR_wos[0][2],lines_CR_wos[0][3], lines_CR_wos[0][4], lines_CR_wos[0][5]))
                    for line in lines_CR_wos[1:]:
                        line[3] = line[3].replace(' ', '')
                        line[4] = line[4].replace(' ', '')
                        Lines_wos.append('   %s, %s, %s, V%s, P%s, %s\n'%(line[0],line[1],line[2],line[3], line[4], line[5]))

                    ## NR
                    Lines_wos.append('NR\n')

                    ## TC
                    lines_TC = [line for line in Lines_section if 'N1  - ' in line]
                    lines_TC = [line for line in lines_TC if 'Cited ' in line]
                    if lines_TC:
                        Lines_wos.append('TC %s' % lines_TC[0][16:])
                    else:
                        Lines_wos.append('TC\n')

                    ## SN
                    lines_SN = [line for line in Lines_section if 'SN  - ' in line]
                    if lines_SN:
                        Lines_wos.append('SN %s' % lines_SN[0][6:])
                    else:
                        Lines_wos.append('SN\n')



                    ## J9
                    lines_J9 = [line for line in Lines_section if 'J2  - ' in line]
                    if lines_J9:
                        Lines_wos.append('J9 %s' % lines_J9[0][6:])
                    else:
                        Lines_wos.append('J9\n')


                    ## PY
                    lines_PY = [line for line in Lines_section if 'PY  - ' in line]
                    if lines_PY:
                        Lines_wos.append('PY %s' % lines_PY[0][6:])
                    else:
                        Lines_wos.append('PY\n')

                    ## VL
                    lines_VL = [line for line in Lines_section if 'VL  - ' in line]
                    if lines_VL:
                        Lines_wos.append('VL %s' % lines_VL[0][6:])
                    else:
                        Lines_wos.append('VL\n')

                    ## IS
                    lines_IS = [line for line in Lines_section if 'IS  -  ' in line]
                    if lines_IS:
                        Lines_wos.append('IS %s' % lines_IS[0][6:])
                    else:
                        Lines_wos.append('IS\n')

                    ## BP
                    lines_BP = [line for line in Lines_section if 'SP  - ' in line]
                    if lines_BP:
                        Lines_wos.append('BP %s' % lines_BP[0][6:])
                    else:
                        Lines_wos.append('BP\n')

                    ## EP
                    lines_EP = [line for line in Lines_section if 'EP  - ' in line]
                    if lines_EP:
                        Lines_wos.append('EP %s' % lines_EP[0][6:])
                    else:
                        Lines_wos.append('EP\n')

                    ## DI
                    lines_DI = [line for line in Lines_section if 'DO  - ' in line]
                    if lines_DI:
                        Lines_wos.append('DI %s' % lines_DI[0][6:])
                    else:
                        Lines_wos.append('DI\n')

                    Lines_wos.append('ER\n')
                    Lines_wos.append('\n')
                    Lines_section = []

                    process = True

        with open('wos1.txt', 'w') as f:
            f.writelines(Lines_wos)

    except Exception as e:
        raise e


if __name__ == '__main__':
    Scopus2HistCite()