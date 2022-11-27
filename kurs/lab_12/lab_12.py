"""
Given the csv file. The task is

analyze the data by weeks (average frequency of alerts per week, their length)
analyze the data by days of the week (which day of the week has more air raid alerts or when their length
has the greatest value)
find the day(s) with the greatest number of the alerts
find the day(s) with the longest alert
depict the data of alerts on plot (choose any criteria for depicting you want)

Additional tasks:

analyze which weeks have more alerts the ones that in the beginning of month, in the middle or in the end
find the region that has the greatest number of alerts
analyze the alerts condition in your own region
"""
import matplotlib.pyplot as plt
import pandas as pd
import pprint
import calendar
from datetime import datetime, timedelta


def convert_str_to_date(date: str, with_time=True) -> datetime:
    return datetime.strptime(date[:-6], '%Y-%m-%d %H:%M:%S') if with_time else \
        datetime.strptime(date[:-15], '%Y-%m-%d')


def convert_date_to_str(date: datetime, with_time=True) -> str:
    return date.strftime('%Y-%m-%d %H:%M:%S') if with_time else date.strftime('%Y-%m-%d')


def get_week_day_by_date(date: str) -> int:
    date = datetime.strptime(date[:-15], '%Y-%m-%d')
    return datetime.weekday(date)


def get_path_of_month_by_date(date: str) -> str:
    date = datetime.strptime(date[:-15], '%Y-%m-%d')
    cur_day = date.day
    if cur_day <= 10:
        return 'beginning'
    elif cur_day <= 20:
        return 'middle'
    else:
        return 'end'


def get_first_and_last_day_month(date: datetime) -> (datetime, datetime):
    year = date.year
    month = date.month
    num_days = calendar.monthrange(year, month)
    first_day = datetime(year, month, 1, 0, 0)
    last_day = datetime(year, month, num_days[1], 0, 0)
    return first_day, last_day


def add_interval_alerts_to_data(data: pd) -> pd:
    return data.assign(
        interval_alerts=data['finished_at'].apply(convert_str_to_date) - data['started_at'].apply(convert_str_to_date))


def add_day_of_week(data: pd) -> pd:
    return data.assign(
        day_of_week=data['started_at'].apply(get_week_day_by_date))


def add_path_of_month(data: pd) -> pd:
    return data.assign(
        path_of_month=data['started_at'].apply(get_path_of_month_by_date))


def add_num_for_sum(data: pd) -> pd:
    return data.assign(num_for_sum=1)


def get_analyze_by_week(data: pd, l_level=('oblast',)) \
        -> {str: {(datetime, datetime): {str: {str: [int, str, timedelta], }, }, }, }:
    """analyze the data by weeks (average frequency of alerts per week, their length)"""
    res_dict = {}
    date_start = data['started_at'].min()
    date_end = data['started_at'].max()
    date_start_dt = convert_str_to_date(date_start, False)
    date_end_dt = convert_str_to_date(date_end, False)
    date_start_week_dt = date_start_dt

    if datetime.weekday(date_start_week_dt):
        while datetime.weekday(date_start_week_dt):
            date_start_week_dt -= timedelta(days=1)

    data_with_interval_alerts = add_interval_alerts_to_data(data)

    for level in l_level:
        level_dict = {}
        data_by_level = data_with_interval_alerts[data_with_interval_alerts['level'] == level]
        temp_date_start_week_dt = date_start_week_dt

        while temp_date_start_week_dt <= date_end_dt:
            region_dict = {}
            date_start_week = convert_date_to_str(temp_date_start_week_dt, False)
            date_end_week_dt = temp_date_start_week_dt + timedelta(weeks=1)
            date_end_week = convert_date_to_str(date_end_week_dt, False)
            data_by_interval_date = data_by_level[
                (data_by_level["started_at"] >= date_start_week) & (data_by_level["started_at"] <= date_end_week)]
            if data_by_interval_date.empty:
                temp_date_start_week_dt += timedelta(weeks=1)
                continue
            temp_dict = data_by_interval_date.to_dict('list')
            temp_dict[level] = set(temp_dict[level])

            for name_region in temp_dict[level]:
                region_data = data_by_interval_date[data_by_interval_date[level] == name_region]
                col_alerts = len(region_data)
                length_alerts = pd.to_timedelta(region_data['interval_alerts']).sum()
                temp = pd.to_numeric(length_alerts.seconds)
                average_length_alerts = f'{int(temp / 7 // 3600)} hours ' \
                                        f'{int(temp /7 % 3600 // 60)} minutes' \
                                        f' {int(temp / 7 % 3600 % 60)} seconds'
                region_dict[name_region] = {'col alerts': col_alerts,
                                            'average alerts frequency': round(col_alerts / 7, 2),
                                            'length alerts': length_alerts,
                                            'average length alerts by day': average_length_alerts}

            level_dict[(temp_date_start_week_dt, date_end_week_dt)] = region_dict
            temp_date_start_week_dt += timedelta(weeks=1)
        res_dict[level] = level_dict

    return res_dict


def get_analyze_by_day_of_week(data: pd, l_level=('oblast',)) \
        -> {(str, datetime, datetime): {str: {int: {str: [int, timedelta]}, }, }, }:
    """
        analyze the data by days of the week (which day of the week has more air raid alerts or when their length
        has the greatest value)
    """
    res_dict = {}
    date_start = data['started_at'].min()
    date_end = data['started_at'].max()
    date_start_dt = convert_str_to_date(date_start, False)
    date_end_dt = convert_str_to_date(date_end, False)

    data_to_work = add_day_of_week(data)
    data_to_work = add_interval_alerts_to_data(data_to_work)

    for level in l_level:
        level_dict = {}
        data_by_level = data_to_work[data_to_work['level'] == level]
        dict_data = data_by_level.to_dict('list')
        dict_data[level] = set(dict_data[level])
        for name_region in dict_data[level]:
            region_data = data_by_level[data_by_level[level] == name_region]
            region_dict = {}
            for day_of_week in range(7):
                day_data = region_data[(region_data['day_of_week'] == day_of_week)]
                if day_data.empty:
                    continue
                col_alerts = len(day_data)
                length_alerts = pd.to_timedelta(day_data['interval_alerts']).sum()
                region_dict[day_of_week] = {'col alerts': col_alerts, 'length alerts': length_alerts}
            level_dict[name_region] = region_dict
        res_dict[(level, date_start_dt, date_end_dt)] = level_dict

    return res_dict


def get_days_with_col_and_length_alerts(data: pd, l_level=('oblast',)) \
        -> {str: {datetime: {str: [int, timedelta]}, }, }:
    """
        find the day(s) with the greatest number of the alerts
    """
    res_dict = {}

    date_start = data['started_at'].min()
    date_end = data['started_at'].max()
    date_end_dt = convert_str_to_date(date_end, False)
    data_with_interval_alerts = add_interval_alerts_to_data(data)

    for level in l_level:
        date_cur_dt = convert_str_to_date(date_start, False)
        level_dict = {}
        data_by_level = data_with_interval_alerts[data_with_interval_alerts['level'] == level]
        while date_cur_dt < date_end_dt:
            date_next_dt = date_cur_dt + timedelta(days=1)
            temp_data = data_by_level[
                (data_by_level['started_at'] >= convert_date_to_str(date_cur_dt)) &
                (data_by_level['started_at'] < convert_date_to_str(date_next_dt))]
            if temp_data.empty:
                date_cur_dt = date_next_dt
                continue
            max_length_alerts = pd.to_timedelta(temp_data['interval_alerts']).max()
            for_info_data = temp_data[temp_data['interval_alerts'] == max_length_alerts]
            for_info_data = for_info_data.to_dict('list')
            level_dict[date_cur_dt] = {'col alerts': len(temp_data.index),
                                       f"max length alerts in {for_info_data['oblast'][0]},"
                                       f" {for_info_data['raion'][0]},"
                                       f" {for_info_data['hromada'][0]}": max_length_alerts}
            date_cur_dt = date_next_dt
        res_dict[level] = level_dict

    return res_dict


def get_max_length_of_alerts(data: pd, l_level=('oblast',)) -> {(), }:
    """
        find the day(s) with the longest alert
    """
    res_dict = {}
    data_with_interval_alerts = add_interval_alerts_to_data(data)
    for level in l_level:
        data_by_level = data_with_interval_alerts[data_with_interval_alerts['level'] == level]
        temp = data_by_level[(data_by_level['interval_alerts'] == data_by_level['interval_alerts'].max())]
        temp = temp.to_dict('list')
        res_temp = []
        for value in temp.values():
            res_temp.append(value[0])
        res_dict[level] = tuple(res_temp)

    return res_dict


def get_analyze_by_path_month(data: pd, l_level=('oblast',)) \
        -> {str: {(datetime, datetime): {str: {str: int, }, }, }, }:
    """
        analyze which weeks have more alerts the ones that in the beginning of month, in the middle or in the end
    """
    res_dict = {}
    date_start = data['started_at'].min()
    date_end = data['started_at'].max()
    date_start_dt = convert_str_to_date(date_start, False)
    date_end_dt = convert_str_to_date(date_end, False)

    data_with_path_of_month = add_path_of_month(data)

    for level in l_level:
        level_dict = {}
        data_by_level = data_with_path_of_month[data_with_path_of_month['level'] == level]
        temp_date_start_week_dt = date_start_dt

        while temp_date_start_week_dt < date_end_dt:
            region_dict = {}
            date_start_month, date_end_month = get_first_and_last_day_month(temp_date_start_week_dt)
            temp_date_start_week_dt = date_end_month + timedelta(days=1)
            data_by_month = data_with_path_of_month[
                (data_with_path_of_month['started_at'] >= convert_date_to_str(date_start_month)) &
                (data_with_path_of_month['started_at'] <= convert_date_to_str(date_end_month))]
            dict_data = data_by_level.to_dict('list')
            dict_data[level] = set(dict_data[level])
            for name_region in dict_data[level]:
                data_by_region = data_by_month[data_by_month[level] == name_region]
                if data_by_region.empty:
                    continue
                beginning_col_alerts = len(data_by_region[data_by_region['path_of_month'] == 'beginning'])
                middle_col_alerts = len(data_by_region[data_by_region['path_of_month'] == 'middle'])
                end_col_alerts = len(data_by_region[data_by_region['path_of_month'] == 'end'])
                region_dict[name_region] = {'0_beginning': beginning_col_alerts,
                                            '1_middle': middle_col_alerts,
                                            '2_end': end_col_alerts}
            level_dict[(date_start_month, date_end_month)] = region_dict
        res_dict[level] = level_dict

    return res_dict


def get_region_with_max_alerts(data: pd, l_level=('oblast',)) -> {str: {str: int}, }:
    """
        find the region that has the greatest number of alerts
    """
    res_dict = {}
    for level in l_level:
        data_by_level = data[data['level'] == level]
        data_by_level = add_num_for_sum(data_by_level)
        temp = data_by_level.groupby(level).sum(numeric_only=True)
        temp = temp[temp['num_for_sum'] == temp['num_for_sum'].max()]
        temp = temp.to_dict()
        res_dict[level] = temp.get('num_for_sum')

    return res_dict


def show_plot(data: pd) -> None:
    """
    depict the data of alerts on plot (choose any criteria for depicting you want)

    analyze the alerts condition in your own region
    """
    l_region = ('Odeska oblast', 'Zakarpatska oblast', 'Kyiv City', 'Kyivska oblast', 'Kharkivska oblast',
                'Dnipropetrovska oblast')

    get_data = get_analyze_by_week(data)
    get_data = get_data['oblast']
    dict_data = {}
    for region in l_region:
        dict_data[region] = {'day': [], 'col_alerts': [], 'length_alerts': []}
        for key, value in get_data.items():
            if value.get(region):
                dict_data[region]['day'].append(
                    f"{datetime.strftime(key[0], '%d')}-{datetime.strftime(key[1], '%d.%m')}")
                dict_data[region]['col_alerts'].append(value[region]['col alerts'])
                dict_data[region]['length_alerts'].append(value[region]['length alerts'].seconds / 3600)

    plot_col_alerts = []
    plot_length_alerts = []
    list_region = []
    for region, value in dict_data.items():
        plot_col_alerts.append((value['day'], value['col_alerts']))
        plot_length_alerts.append((value['day'], value['col_alerts']))
        list_region.append(region)

    create_plot(title="Number of alarms", x_label="Date", y_label="Number of alarms per week",
                data_plot=plot_col_alerts, l_legend=list_region, part_save="plot/col_alerts.png")

    create_plot(title="Length of alarms", x_label="Date", y_label="Length of alarms per week, hours",
                data_plot=plot_length_alerts, l_legend=list_region, part_save="plot/length_alerts.png")


def create_plot(title, x_label, y_label, data_plot, l_legend, part_save, size=(40, 5)):
    plt.figure(figsize=size)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    for data_ax in data_plot:
        plt.plot(data_ax[0], data_ax[1])
    plt.legend(l_legend, loc='upper left')
    plt.savefig(part_save)


if __name__ == "__main__":

    try:
        data_pd = pd.read_csv('https://raw.githubusercontent.com'
                              '/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets'
                              '/full_data.csv?fbclid=PAAaY5H2U_sD9OaCQLZhl2r5KZs7xfUuVRoIvPdpG1oIV2yXimmE9jD1h27io')
    except:
        data_pd = pd.read_csv("data_pd.csv")

    pp = pprint.PrettyPrinter()

    pp.pprint(get_analyze_by_week(data_pd))

    #pp.pprint(get_analyze_by_day_of_week(data_pd))

    #pp.pprint(get_days_with_col_and_length_alerts(data_pd))

    #pp.pprint(get_analyze_by_path_month(data_pd))

    #pp.pprint(get_region_with_max_alerts(data_pd, ('oblast', 'raion', 'hromada')))

    #show_plot(data_pd)
