# import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling
import pf_5_export_EDA_xlsxwriter as xcs

# load dataset
file_path = 'path_to_your_file.xlsx'
sheet_name = 'Arkusz1'

df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
descr = pd.read_excel(file_path, sheet_name=sheet_name, nrows=1)

# set auxiliary variables for df manipulation
metrics = list(df.loc[:, df.columns.str.startswith('M')].columns.values)
positions = list(df.loc[:, df.columns.str.startswith('p')].columns.values)

# set auxiliary variables for descr manipulations
col_descr = list(descr.values[0].tolist())
col_names = list(descr.columns.values.tolist())
ops = dict(zip(col_descr, col_names))

# drop unused columns from descr list
opisy = ops.copy()
for key in ops.keys():  # drop
    if (key not in metrics+positions):
        opisy.pop(key, None)

# set proper dataframes to work with
df['Submitted'] = pd.to_datetime(df['Submitted'])
data = df[['Submitted'] + positions + metrics]

# print(data.dtypes)
# print(df.head(5))
# print(data.head(5))

# profiling the dataset
# print(data.info())
# print(pandas_profiling.ProfileReport(data))

profile = pandas_profiling.ProfileReport(data)
profile.to_file('report.html')

writer = pd.ExcelWriter('path_to_file.xlsx', engine='xlsxwriter')
workbook = writer.book
chart_num = 1
MS_colors = ['#5E9CD3', '#ED7D31', '#A5A5A5', '#FFC001', '#4472C4',
             '#70AD47', '#44546A', '#1E4E79', "#833C0B", '#525252',
             '#7F6000', '#1F3864', '#375623', '#222A35', '#9cc2e4',
             '#f3b183', '#c9c9c9', '#ffd965', '#8eaadb', '#a8d08d',
             '#8496b0']


for item in positions+metrics:
    worksheet = workbook.add_worksheet(item)
    writer.sheets[item] = worksheet

    pivot_a = pd.Series(data[item].value_counts(normalize=False), name='n')
    pivot_b = pd.Series(data[item].value_counts(normalize=True), name='%')

    sum_n = pivot_a.sum()
    sum_p = pivot_b.sum()

    pivot_c = pd.Series([sum_n, sum_p], ['n', '%'], name='total')

    pivot_abc = pd.concat([pivot_b, pivot_a], axis=1).append(pivot_c)
    pivot_abc['n'] = pivot_abc['n'].astype(int)
    pivot_abc['%'] = pivot_abc['%'].round(17)

    # add description in first row
    init_space = 0
    worksheet.write_string(init_space, 0, opisy.get(item))
    init_space += 1

    # add item name in second row
    worksheet.write_string(init_space, 0, item)
    init_space += 1

    # add chart title
    chart_title = 'Chart no ' + \
        str(chart_num) + '. ' + opisy.get(item) + \
        ' (N-' + str(pivot_abc.iloc[-1, -1]) + ')'
    worksheet.write_string(init_space, 0, chart_title)
    init_space += 1
    chart_num += 1

    # add first df to worksheet
    pivot_abc.to_excel(writer, sheet_name=item,
                       startrow=init_space, startcol=1)

    # add chart linked to first df
    chart = workbook.add_chart({'type': 'column'})

    for col in range(pivot_abc.shape[1]-1):
        series_data = {
            'name': [item, init_space, 2],
            'categories': [item, init_space + 1, 1,
                           init_space + pivot_abc.shape[0] - 1, 1],
            'values': [item, init_space + 1, col + 2,
                       init_space + pivot_abc.shape[0] - 1, col + 2],
            'fill': {'color': MS_colors[col]},
        }
        series_input = dict(series_data, **xcs.series)
        chart.add_series(series_input)

    xcs.chart_col(item=chart, title=chart_title)
    worksheet.insert_chart(init_space, pivot_abc.shape[1]+3, chart)

    init_space += pivot_abc.shape[0] + 11

    for num, metric in enumerate(metrics):
        if item != metric:
            pivot_d = pd.crosstab(
                index=data[item], columns=data[metric],
                margins=False, margins_name='total')
            # pivot_d.drop(pivot_d.index[2], inplace=True)  # drop cols if any

            # dynamic sum instead static margins
            pivot_d['total'] = pivot_d.sum(axis=1)
            pivot_d = pivot_d.sort_values(
                by=['total', item], axis=0, ascending=False)
            pivot_d.loc['total', :] = pivot_d.sum(axis=0)
            pivot_e = (pivot_d/pivot_d.loc['total']).round(17)

            seria_n = pd.Series(data[metric].value_counts(
                normalize=False), name='n')
            seria_n['total'] = seria_n.sum()
            pivot_e.loc['n', :] = seria_n

            # add item name vs metric cross
            worksheet.write_string(init_space, 0, item + " x " + metric)
            init_space += 1

            # add chart title
            for key, val in ops.items():
                if key == metric:
                    chart_title = 'Chart no ' + str(chart_num) + \
                        '. ' + opisy.get(item) + " - by " + \
                        val.lower() + \
                        ' (N-' + str(pivot_abc.iloc[-1, -1]) + ')'
                    worksheet.write_string(init_space, 0, chart_title)
                    init_space += 1
                    chart_num += 1

            # add next df to worksheet
            pivot_e.to_excel(writer, sheet_name=item,
                             startrow=init_space, startcol=1)
            chart = workbook.add_chart({'type': 'column'})

            for col in range(pivot_e.shape[1]-1):
                series_data = {
                    'name': [item, init_space, col+2],
                    'categories': [item, init_space + 1, 1,
                                   init_space + pivot_e.shape[0] - 2, 1],
                    'values': [item, init_space + 1, col + 2,
                               init_space + pivot_e.shape[0] - 2, col + 2],
                    'fill': {'color': MS_colors[col]},
                }
                series_input = dict(series_data, **xcs.series)
                chart.add_series(series_input)

            xcs.chart_col(item=chart, title=chart_title)
            worksheet.insert_chart(init_space, pivot_e.shape[1]+3, chart)

            init_space += pivot_e.shape[0]+11

writer.save()
