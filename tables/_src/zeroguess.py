'''Generates a LaTeX table from the numerical data.'''

import tabulate
import json


# a hack to define a missing table format
tabulate._table_formats['latex_booktabs_raw'] = tabulate.TableFormat(
        lineabove=tabulate.partial(tabulate._latex_line_begin_tabular, booktabs=True),
        linebelowheader=tabulate.Line("\\midrule", "", "", ""),
        linebetweenrows=None,
        linebelow=tabulate.Line("\\bottomrule\n\\end{tabular}", "", "", ""),
        headerrow=tabulate.partial(tabulate._latex_row, escrules={}),
        datarow=tabulate.partial(tabulate._latex_row, escrules={}),
        padding=1,
        with_header_hide=None,
    )

headers = [
            r'$P_\text{YAG}$', 
            r'$T$',
            # r'penetration',
            r'welding depth',
            r'$J_\text{penetration}$',
            r'$J_\text{velocity}$',
            r'$J_\text{completeness}$',
            r'$J_\text{control}$',
            r'$J_\text{total}$',
          ]

# warning: the next code block is duplicated in two scripts
# move it to a separate module (DRY)
powers = [1500, 2000, 2500]
times =  [0.010, 0.015, 0.020]

report_files = [
        f'numericals/zeroguess/{P_YAG}-{T:5.3f}.json'
            for T in times for P_YAG in powers
        ]
########################################

def get_line(filename):
    with open(filename) as file:
        report = json.load(file)
    return report.values()

lines = [get_line(filename) for filename in report_files]

table = tabulate.tabulate(
        lines,
        headers=headers,
        tablefmt='latex_booktabs_raw',
        colalign=('center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'),
        floatfmt=('.3f', '.3f', '.1f', '.4f', '.4f',  '.4f',  '.4f',  '.4f'),
    )

print(table)

# TODO: add color highlighting for critical values
