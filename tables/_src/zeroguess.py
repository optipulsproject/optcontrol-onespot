'''Generates a LaTeX table from the numerical data.'''

import tabulate
import json

import optenv.parameters

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


powers = optenv.parameters.zeroguess['powers']
times = optenv.parameters.zeroguess['times']

report_files = [
        filename.replace('.npy', '.json')
        for filename in optenv.parameters.zeroguess['optcontrols']
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
        floatfmt=('.3f', '.3f', '.7f', '.4f', '.4f',  '.4f',  '.4f',  '.4f'),
    )

print(table)

# TODO: add color highlighting for critical values
