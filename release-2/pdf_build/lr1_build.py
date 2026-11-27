from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.chart import BarChart, ScatterChart, Reference, Series
from openpyxl.comments import Comment

vals=[87,119,85,52,78,39,99,56,53,74,108,47,61,101,56,79,42,52,30,100,50,34,85,99,71,113,67,83,88,98]
A="Arial"
f=lambda **k: Font(name=A,size=k.pop("size",10),**k)
thin=Side(style="thin",color="000000"); BR=Border(left=thin,right=thin,top=thin,bottom=thin)
HDR=PatternFill("solid",fgColor="DCE6F1"); INP=PatternFill("solid",fgColor="FFFF99")
ctr=Alignment(horizontal="center",vertical="center",wrap_text=True)
wb=Workbook()

# ---------------- Титул ----------------
t=wb.active; t.title="Титул"
t["A1"]="Лабораторная работа №1"; t["A1"].font=f(bold=True,size=16)
t["A2"]="Группировка, построение гистограммы и полигона распределения в Excel"; t["A2"].font=f(bold=True,size=12)
rows=[("Студент(ка) группы:","______________"),("Вариант:","5 (столбец «5» из файла «ЛР 1 Задания»)"),("Год:","2026")]
for i,(a,b) in enumerate(rows,4):
    t.cell(i,1,a).font=f(bold=True); t.cell(i,2,b).font=f()
t["A8"]="Цель работы"; t["A8"].font=f(bold=True,size=11)
t["A9"]="Первичная статистическая обработка данных: группировка ряда, построение интервального ряда, гистограммы (по частотам), полигона (по относительным частотам), расчёт среднего, дисперсии и СКО двумя способами: функциями Excel и «Пакетом анализа»."
t["A9"].alignment=Alignment(wrap_text=True,vertical="top"); t["A9"].font=f(); t.merge_cells("A9:F9"); t.row_dimensions[9].height=48
t["A11"]="Состав книги"; t["A11"].font=f(bold=True,size=11)
for i,(a,b) in enumerate([("Данные","исходный ряд варианта 5 (жёлтые ячейки можно менять/дополнять)"),("Расчёт","способ (а): функции МИН, МАКС, ЧАСТОТА, СРЗНАЧ, ДИСП, КОРЕНЬ; гистограмма и полигон"),("Пакет анализа","способ (б): результат инструмента «Гистограмма» и сравнение со способом (а)"),("Выводы","анализ полученных данных")],12):
    t.cell(i,1,a).font=f(bold=True); t.cell(i,2,b).font=f()
t["A17"]="ВАЖНО"; t["A17"].font=f(bold=True,color="C00000")
t["A18"]=("В скриншоте задания не видны строки №1–3 (скрыты), поэтому использованы 30 видимых значений (№4–33). "
          "Если в исходном файле значения №1–3 есть, допишите их в столбец B листа «Данные» (в пустые жёлтые ячейки ниже): все расчёты, таблицы и графики пересчитаются автоматически.")
t["A18"].alignment=Alignment(wrap_text=True,vertical="top"); t["A18"].font=f(color="C00000"); t.merge_cells("A18:F18"); t.row_dimensions[18].height=62
t.column_dimensions["A"].width=24; t.column_dimensions["B"].width=70
for c in "CDEF": t.column_dimensions[c].width=10

# ---------------- Данные ----------------
d=wb.create_sheet("Данные")
d["A1"]="Исходные данные, вариант 5"; d["A1"].font=f(bold=True,size=12)
d["A2"]="Источник: скриншот файла «ЛР 1 Задания», столбец «5». Номера сохранены как в файле (с №4)."; d["A2"].font=f(italic=True,size=9)
d["A3"]="Жёлтые ячейки (B5:B64) — ввод. Пустые ячейки игнорируются расчётами."; d["A3"].font=f(italic=True,size=9)
for c,txt in (("A4","№"),("B4","Значение xᵢ")):
    d[c]=txt; d[c].font=f(bold=True); d[c].fill=HDR; d[c].alignment=ctr; d[c].border=BR
for i in range(60):
    r=5+i
    d.cell(r,1,i+4 if i<30 else None).font=f(); d.cell(r,1).border=BR
    c=d.cell(r,2,vals[i] if i<30 else None); c.font=f(color="0000FF"); c.fill=INP; c.border=BR
d.column_dimensions["A"].width=8; d.column_dimensions["B"].width=16
d.freeze_panes="A5"
DATA="Данные!$B$5:$B$64"

# ---------------- Расчёт ----------------
s=wb.create_sheet("Расчёт")
s["A1"]="Способ (а): расчёт встроенными функциями Excel"; s["A1"].font=f(bold=True,size=13)
def lab(r,txt,fml,fmt=None,note=None):
    s.cell(r,1,txt).font=f(); s.cell(r,1).border=BR
    c=s.cell(r,2,fml); c.font=f(); c.border=BR; c.alignment=Alignment(horizontal="right")
    if fmt: c.number_format=fmt
s["A3"]="1. Параметры выборки и интервалов"; s["A3"].font=f(bold=True,size=11)
lab(4,"Объём выборки N  =СЧЁТ()",f"=COUNT({DATA})","0")
lab(5,"xmin  =МИН()",f"=MIN({DATA})","0")
lab(6,"xmax  =МАКС()",f"=MAX({DATA})","0")
lab(7,"Размах R = xmax − xmin","=B6-B5","0")
lab(8,"Формула Стерджесса: 1 + 3,322·lg N","=1+3.322*LOG10(B4)","0.000")
lab(9,"Число интервалов n (округлено)","=ROUND(B8,0)","0")
lab(10,"Величина интервала h = (xmax − xmin)/n","=B7/B9","0.0000")
s["A11"]="Контроль числа строк таблицы"; s["A11"].font=f(italic=True,size=9)
s["B11"]='=IF(B9=6,"OK: n = 6, таблица рассчитана на 6 интервалов","Число интервалов изменилось: добавьте или удалите строки таблицы")'; s["B11"].font=f(italic=True,size=9)

s["A13"]="2. Интервальный ряд распределения"; s["A13"].font=f(bold=True,size=11)
hdr=["№","Левая граница","Правая граница (карман)","Интервал (подпись)","Середина интервала","Частота mᵢ  =ЧАСТОТА()","Относит. частота Wᵢ = mᵢ/N"]
for j,h in enumerate(hdr,1):
    c=s.cell(14,j,h); c.font=f(bold=True); c.fill=HDR; c.alignment=ctr; c.border=BR
s.row_dimensions[14].height=44
for i in range(6):
    r=15+i
    s.cell(r,1,i+1)
    s.cell(r,2,"=$B$5" if i==0 else f"=C{r-1}")
    s.cell(r,3,f"=$B$5+A{r}*$B$10" if i<5 else "=$B$6")
    s.cell(r,4,f'=ROUND(B{r},1)&"–"&ROUND(C{r},1)')
    s.cell(r,5,f"=(B{r}+C{r})/2")
    s.cell(r,7,f"=F{r}/$B$4")
    for j in range(1,8):
        c=s.cell(r,j); c.font=f(); c.border=BR
        c.alignment=Alignment(horizontal="center")
    for j in (2,3,5): s.cell(r,j).number_format="0.00"
    s.cell(r,7).number_format="0.0000"
s["F15"]=ArrayFormula("F15:F21",f"=FREQUENCY({DATA},$C$15:$C$20)")
for r in range(15,22):
    c=s.cell(r,6); c.font=f(); c.border=BR; c.alignment=Alignment(horizontal="center"); c.number_format="0"
s["A21"]="Еще"; s["D21"]="значений > последней границы"
for j in (1,4):
    s.cell(21,j).font=f(italic=True,size=9); s.cell(21,j).border=BR
for j in (2,3,5,7): s.cell(21,j).border=BR
s["A22"]="Σ"; s["F22"]="=SUM(F15:F20)"; s["G22"]="=SUM(G15:G20)"
for j in range(1,8): s.cell(22,j).border=BR; s.cell(22,j).font=f(bold=True)
s["F22"].alignment=Alignment(horizontal="center"); s["G22"].alignment=Alignment(horizontal="center"); s["G22"].number_format="0.0000"
s["A23"]='=IF(AND(F22+F21=B4,ROUND(G22,10)=1),"Контроль: Σmᵢ = N и ΣWᵢ = 1 — выполнен","ОШИБКА контроля: Σmᵢ ≠ N")'; s["A23"].font=f(italic=True,size=9)
s["A24"]="Последняя правая граница = МАКС() (не xmin + n·h), чтобы избежать ошибки округления: вычисленное число могло бы оказаться чуть меньше xmax и значение не попало бы в интервал."
s["A24"].font=f(italic=True,size=9)

s["A26"]="3. Числовые характеристики выборки"; s["A26"].font=f(bold=True,size=11)
lab(27,"Среднее арифметическое x̄  =СРЗНАЧ()",f"=AVERAGE({DATA})","0.0000")
lab(28,"Дисперсия D  =ДИСП() (по выборке, n−1)",f"=VAR({DATA})","0.0000")
lab(29,"Среднее квадратическое отклонение σ = √D  =КОРЕНЬ()","=SQRT(B28)","0.0000")
lab(30,"Дисперсия Dв  =ДИСПР() (формула (5): 1/N)",f"=VARP({DATA})","0.0000")
lab(31,"СКО по Dв:  σв = √Dв","=SQRT(B30)","0.0000")
lab(32,"Медиана  =МЕДИАНА()",f"=MEDIAN({DATA})","0.0")
lab(33,"Коэффициент вариации σ/x̄","=B29/B27","0.0%")
lab(34,"Модальный интервал (макс. частота)","=INDEX(D15:D20,MATCH(MAX(F15:F20),F15:F20,0))")
s["A35"]="Инструкция требует ДИСП (дисперсия по выборке, n−1); формула (5) в теории — с делителем N. Приведены обе."; s["A35"].font=f(italic=True,size=9)

s.column_dimensions["A"].width=50
for c,w in zip("BCDEFG",(18,20,20,16,18,18)): s.column_dimensions[c].width=w

# charts
ch=BarChart(); ch.type="col"; ch.title="Гистограмма распределения по частотам"
ch.add_data(Reference(s,min_col=6,min_row=15,max_row=20),titles_from_data=False)
ch.set_categories(Reference(s,min_col=4,min_row=15,max_row=20))
ch.gapWidth=0; ch.legend=None; ch.roundedCorners=False
ch.x_axis.title="Интервалы"; ch.y_axis.title="Частота mᵢ"
ch.x_axis.delete=False; ch.y_axis.delete=False
ch.series[0].graphicalProperties.solidFill="4F81BD"; ch.series[0].graphicalProperties.line.solidFill="000000"
ch.height=8.5; ch.width=16
s.add_chart(ch,"I3")
sc=ScatterChart(); sc.title="Полигон распределения по относительным частотам"; sc.style=13
x=Reference(s,min_col=5,min_row=15,max_row=20); y=Reference(s,min_col=7,min_row=15,max_row=20)
se=Series(y,x,title="Wᵢ"); se.marker.symbol="circle"; se.marker.size=7; se.smooth=False
se.graphicalProperties.line.solidFill="C0504D"; se.graphicalProperties.line.width=22000
sc.series.append(se); sc.legend=None; sc.roundedCorners=False
sc.x_axis.title="Середина интервала"; sc.y_axis.title="Относительная частота Wᵢ"
sc.x_axis.delete=False; sc.y_axis.delete=False
sc.height=8.5; sc.width=16
s.add_chart(sc,"I22")

# ---------------- Пакет анализа ----------------
p=wb.create_sheet("Пакет анализа")
p["A1"]="Способ (б): инструмент «Гистограмма» надстройки «Пакет анализа»"; p["A1"].font=f(bold=True,size=13)
p["A2"]=("Параметры инструмента: Входной интервал — Данные!B5:B64; Интервал карманов — правые границы (лист «Расчёт», C15:C20); флажок «Вывод графика». "
         "Здесь воспроизведён формат вывода инструмента (столбцы «Карман» и «Частота», строка «Еще»); значения посчитаны формулами и сравниваются со способом (а).")
p["A2"].alignment=Alignment(wrap_text=True,vertical="top"); p["A2"].font=f(italic=True,size=9); p.merge_cells("A2:E2"); p.row_dimensions[2].height=52
for j,h in enumerate(["Карман","Частота","Частота ЧАСТОТА() (способ а)","Разница"],1):
    c=p.cell(4,j,h); c.font=f(bold=True); c.fill=HDR; c.alignment=ctr; c.border=BR
p.row_dimensions[4].height=40
for i in range(6):
    r=5+i
    p.cell(r,1,f"='Расчёт'!C{15+i}").number_format="0.00"
    p.cell(r,2,f'=COUNTIF({DATA},"<="&A{r})' if i==0 else f'=COUNTIF({DATA},"<="&A{r})-COUNTIF({DATA},"<="&A{r-1})')
    p.cell(r,3,f"='Расчёт'!F{15+i}"); p.cell(r,4,f"=B{r}-C{r}")
p.cell(11,1,"Еще"); p.cell(11,2,f'=COUNTIF({DATA},">"&A10)'); p.cell(11,3,"='Расчёт'!F21"); p.cell(11,4,"=B11-C11")
for r in range(5,12):
    for j in range(1,5):
        c=p.cell(r,j); c.font=f(); c.border=BR; c.alignment=Alignment(horizontal="center")
p["A12"]='=IF(SUMPRODUCT(ABS(D5:D11))=0,"Сравнение: результаты двух способов полностью совпали","Результаты способов различаются")'; p["A12"].font=f(italic=True,size=9)
p.column_dimensions["A"].width=14; p.column_dimensions["B"].width=14; p.column_dimensions["C"].width=24; p.column_dimensions["D"].width=12
ph=BarChart(); ph.type="col"; ph.title="Гистограмма (Пакет анализа)"
ph.add_data(Reference(p,min_col=2,min_row=4,max_row=11),titles_from_data=True)
ph.set_categories(Reference(p,min_col=1,min_row=5,max_row=11))
ph.gapWidth=10; ph.roundedCorners=False; ph.legend.position="b"; ph.legend.overlay=False
ph.x_axis.title="Карман"; ph.y_axis.title="Частота"; ph.x_axis.delete=False; ph.y_axis.delete=False
ph.height=8.5; ph.width=15
p.add_chart(ph,"F4")

# ---------------- Выводы ----------------
v=wb.create_sheet("Выводы")
v["A1"]="Выводы"; v["A1"].font=f(bold=True,size=13)
lines=[
 '="1. Объём выборки N = "&\'Расчёт\'!B4&"; значения лежат в диапазоне от "&\'Расчёт\'!B5&" до "&\'Расчёт\'!B6&" (размах "&\'Расчёт\'!B7&")."',
 '="2. По формуле Стерджесса получено n = "&\'Расчёт\'!B9&" интервалов, величина интервала h = "&ROUND(\'Расчёт\'!B10,3)&"."',
 '="3. Наибольшая частота у интервала "&\'Расчёт\'!B34&" (mᵢ = "&MAX(\'Расчёт\'!F15:F20)&", Wᵢ = "&ROUND(MAX(\'Расчёт\'!F15:F20)/\'Расчёт\'!B4,3)&"). Сумма частот равна N, сумма относительных частот равна 1."',
 '="4. Среднее арифметическое x̄ = "&ROUND(\'Расчёт\'!B27,2)&", медиана = "&ROUND(\'Расчёт\'!B32,2)&": значения близки, поэтому распределение примерно симметрично."',
 '="5. Дисперсия D = "&ROUND(\'Расчёт\'!B28,2)&" (ДИСП, n−1), Dв = "&ROUND(\'Расчёт\'!B30,2)&" (с делителем N); СКО σ = "&ROUND(\'Расчёт\'!B29,2)&", коэффициент вариации "&ROUND(\'Расчёт\'!B33*100,1)&"% — разброс значений большой, выборка неоднородна."',
 '="6. Гистограмма и полигон не имеют одного выраженного пика (частоты интервалов 4–7 меняются «волнами»): для выборки из 30 значений форма распределения близка к равномерной, нормальность по графику подтвердить нельзя; для надёжного вывода нужна выборка большего объёма и критерий согласия (лекции 7.1, 7.2)."',
 '="7. Результаты способов (а) и (б) "&IF(SUMPRODUCT(ABS(\'Пакет анализа\'!D5:D11))=0,"полностью совпали","различаются")&": «Пакет анализа» и функция ЧАСТОТА используют одно правило подсчёта (значение попадает в интервал, если оно > предыдущего кармана и ≤ текущего)."',
]
for i,l in enumerate(lines,3):
    c=v.cell(i,1,l); c.font=f(); c.alignment=Alignment(wrap_text=True,vertical="top"); v.row_dimensions[i].height=48
v["A11"]="Пункт 6 написан по виду графиков для 30 видимых значений; если вы добавите значения №1–3, перепроверьте формулировку по новым графикам."
v["A11"].font=f(italic=True,size=9,color="C00000")
v.column_dimensions["A"].width=120
wb.save("ЛР1_вариант5.xlsx")
