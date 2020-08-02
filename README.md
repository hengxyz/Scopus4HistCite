# Scopus4HistCite
Changing the format of the reference file *.ris exported from the Scopus to the WOS format which can be completely  analysed by HistCite.

## Why Scopus4HistCite
People can use Scopus4HistCite to transform the refences files exported from Scopus, i.e., scopus.ris, to the WOS format to do the complete reference analysis.

Since the solution of Loet Leydesdorff https://www.leydesdorff.net/scopus/' cannot transform the data in the wos for the local references analysis by HistCite, this solution can generate the complete WOS format data and calibrate the errors of the incorrect or incomplete information such as the author names, years, page numbers and volume numbers, which allow the HistCite or HistCitePro (Thanks to the Author's tutorial https://www.youtube.com/watch?v=6EMwQGYazC0 and the website: https://zhuanlan.zhihu.com/p/20902898 (in Chinese)) search the local references in a high accuracy and employ the local references analysis or draw the HistCite graph.

## How to use:
1) Download the package in Windows;
2) Put the exported Scopus file *.ris in the same directory (you can put serveral *.ris files under the directory, which allows Scopus to split the references in serveral *.ris files to export);
3) Click the Scopus4HistCite.bat; (Or you can click the Scopus2WOS.exe and then click the CorrectScopus2wos_3.exe in case of the failure of Scopus4HistCite.bat)
4) Copy the obtained wos2.txt to ./HistCitePro2.1/TXT/;

Then you can use HistCite to analyse your references in your domaines!



### License
This code is distributed under MIT LICENSE

### Contact
Zuheng Ming
zuheng.ming@univ-lr.fr
