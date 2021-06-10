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
        r'pulse shape', 
        r'temp',
        r'$J_\text{penetration}$',
        r'$J_\text{velocity}$',
        r'$J_\text{completeness}$',
        r'$J_\text{control}$',
        r'$J_\text{ total}$',
        ]

report_files = [
        f'numericals/rampdown/2000-1500-0.005-0.005-0.012.json',
        f'numericals/rampdown/2000-1500-0.005-0.010-0.012.json',
        ]

def get_line(filename):
    with open(filename) as file:
        report = json.load(file)
    return report.values()

# lines = [
#             ['conventional', 0.375, 0, 0, 0, 0, 0],
#             ['opt. conventional', 0.375, 0, 0, 0, 0, 0],
#             ['linear rampdown', 0.375, 0, 0, 0, 0, 0],
#             ['opt. linear rampdown', 0.375, 0, 0, 0, 0, 0],
#         ]

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
