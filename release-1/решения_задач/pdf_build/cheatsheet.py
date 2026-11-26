# Генератор шпаргалки по критериям (XeLaTeX). Запуск: python3 cheatsheet.py && xelatex cheatsheet.tex
from scipy import stats
def c(x,nd=2):
    return f"{x:.{nd}f}".replace(".",",")

def chi_table():
    alphas=[0.995,0.99,0.975,0.95,0.05,0.025,0.01,0.005]
    s="\\begin{tabular}{r|"+"r"*len(alphas)+"}\n$k$"+"".join(f" & {c(a,3)}" for a in alphas)+"\\\\\\hline\n"
    for k in range(1,31):
        s+=f"{k}"+"".join(f" & {c(stats.chi2.ppf(1-a,k),2)}" for a in alphas)+"\\\\\n"
    return s+"\\end{tabular}"

def t_table():
    al=[0.1,0.05,0.02,0.01,0.002,0.001]
    s="\\begin{tabular}{r|"+"r"*len(al)+"}\n$k$"+"".join(f" & {c(a,3)}" for a in al)+"\\\\\\hline\n"
    for k in list(range(1,31))+[40,60,120]:
        s+=f"{k}"+"".join(f" & {c(stats.t.ppf(1-a/2,k),3)}" for a in al)+"\\\\\n"
    s+="$\\infty$"+"".join(f" & {c(stats.norm.ppf(1-a/2),3)}" for a in al)+"\\\\\n"
    return s+"\\end{tabular}"

def f_table(a):
    k1s=[1,2,3,4,5,6,7,8,9,10,12,15,20,24,30]
    k2s=list(range(1,31))+[40,60,120]
    s="\\begin{tabular}{r|"+"r"*len(k1s)+"}\n$k_2\\backslash k_1$"+"".join(f" & {k}" for k in k1s)+"\\\\\\hline\n"
    for k2 in k2s:
        s+=f"{k2}"
        for k1 in k1s:
            v=stats.f.ppf(1-a,k1,k2)
            s+=f" & {c(v,1) if v>=100 else c(v,2)}"
        s+="\\\\\n"
    return s+"\\end{tabular}"

body=open("cheatsheet_body.tex",encoding="utf8").read()
body=body.replace("%%CHI%%",chi_table()).replace("%%T%%",t_table())
for a,key in [(0.05,"F05"),(0.025,"F025"),(0.01,"F01"),(0.005,"F005")]:
    body=body.replace(f"%%{key}%%",f_table(a))
head=open("cheatsheet_head.tex",encoding="utf8").read()
open("cheatsheet.tex","w",encoding="utf8").write(head+body+"\n\\end{document}\n")
