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
import calendar
import matplotlib.pyplot as plt
import pandas as pd
import pprint
from datetime import datetime, timedelta
from urllib.error import URLError


def convert_str_to_date(date: str, with_time=True) -> datetime:
    return datetime.strptime(date[:-6], '%Y-%m-%d %H:%M:%S') if with_time else datetime.strptime(date[:-15], '%Y-%m-%d')


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
        interval_alerts=data['finished_at'].apply(convert_str_to_date) - data['started_at'].apply(convert_str_to_date)
    )


def add_day_of_week(data: pd) -> pd:
    return data.assign(
        day_of_week=data['started_at'].apply(get_week_day_by_date)
    )


def add_path_of_month(data: pd) -> pd:
    return data.assign(
        path_of_month=data['started_at'].apply(get_path_of_month_by_date)
    )


def add_num_for_sum(data: pd) -> pd:
    return data.assign(num_for_sum=1)


def get_date_start_week(date_start_week: datetime) -> datetime:
    while datetime.weekday(date_start_week):
        date_start_week -= timedelta(days=1)
    return date_start_week


def get_regions_analyze_by_week(regions: set, data: pd, level: str) -> dict:
    res_dict = {}
    for region in regions:
        region_data = data[data[level] == region]
        num_alerts = len(region_data)
        length_alerts = pd.to_timedelta(region_data['interval_alerts']).sum()
        temp = pd.to_numeric(length_alerts.seconds)
        average_length_alerts = f'{int(temp / 7 // 3600)} hours ' \
                                f'{int(temp / 7 % 3600 // 60)} minutes' \
                                f' {int(temp / 7 % 3600 % 60)} seconds'
        res_dict[region] = {'num alerts': num_alerts,
                            'average alerts frequency': round(num_alerts / 7, 2),
                            'length alerts': length_alerts,
                            'average length alerts by day': average_length_alerts}
    return res_dict


def get_level_analyze_by_week(date_start: datetime, date_end: datetime, data: pd, level: str) -> dict:
    res_dict = {}

    while date_start <= date_end:
        date_start_week = convert_date_to_str(date_start, False)
        date_end_week = convert_date_to_str(date_start + timedelta(weeks=1), False)
        data_by_interval_date = data[
            (data["started_at"] >= date_start_week) & (data["started_at"] <= date_end_week)]
        if data_by_interval_date.empty:
            date_start += timedelta(weeks=1)
            continue

        regions = set(data_by_interval_date.to_dict('list')[level])
        res_dict[(date_start, date_start + timedelta(weeks=1))] = get_regions_analyze_by_week(
            regions, data_by_interval_date, level
        )

        date_start += timedelta(weeks=1)
    return res_dict


def get_analyze_by_week(data: pd, l_level=('oblast',)) -> dict:
    """analyze the data by weeks (average frequency of alerts per week, their length)"""
    res_dict = {}
    date_start = convert_str_to_date(data['started_at'].min(), False)
    date_end = convert_str_to_date(data['started_at'].max(), False)

    date_start = get_date_start_week(date_start)

    data_with_interval_alerts = add_interval_alerts_to_data(data)

    for level in l_level:
        data_by_level = data_with_interval_alerts[data_with_interval_alerts['level'] == level]
        res_dict[level] = get_level_analyze_by_week(date_start, date_end, data_by_level, level)

    return res_dict


def get_regions_analyze_by_day_of_week(regions: set, data: pd, level: str) -> dict:
    res_dict = {}
    for region in regions:
        region_data = data[data[level] == region]
        region_dict = {}

        for day_of_week in range(7):
            day_data = region_data[(region_data['day_of_week'] == day_of_week)]
            if day_data.empty:
                continue
            num_alerts = len(day_data)
            length_alerts = pd.to_timedelta(day_data['interval_alerts']).sum()
            region_dict[day_of_week] = {'num alerts': num_alerts, 'length alerts': length_alerts}
        res_dict[region] = region_dict

    return res_dict


def get_analyze_by_day_of_week(data: pd, l_level=('oblast',)) -> dict:
    """
        analyze the data by days of the week (which day of the week has more air raid alerts or when their length
        has the greatest value)
    """
    res_dict = {}
    date_start_dt = convert_str_to_date(data['started_at'].min(), False)
    date_end_dt = convert_str_to_date(data['started_at'].max(), False)

    data_to_work = add_day_of_week(data)
    data_to_work = add_interval_alerts_to_data(data_to_work)

    for level in l_level:
        data = data_to_work[data_to_work['level'] == level]
        regions = set(data.to_dict('list')[level])
        res_dict[(level, date_start_dt, date_end_dt)] = get_regions_analyze_by_day_of_week(regions, data, level)

    return res_dict


def get_days_with_num_and_length_alerts_by_level(date_start: datetime, date_end: datetime, data: pd) -> dict:
    res_dict = {}
    while date_start < date_end:
        date_next = date_start + timedelta(days=1)
        temp_data = data[
            (data['started_at'] >= convert_date_to_str(date_start)) &
            (data['started_at'] < convert_date_to_str(date_next))]
        if temp_data.empty:
            date_start = date_next
            continue
        max_length_alerts = pd.to_timedelta(temp_data['interval_alerts']).max()
        for_info_data = temp_data[temp_data['interval_alerts'] == max_length_alerts]
        for_info_data = for_info_data.to_dict('list')
        res_dict[date_start] = {'num alerts': len(temp_data.index),
                                f"max length alerts in {for_info_data['oblast'][0]},"
                                f" {for_info_data['raion'][0]},"
                                f" {for_info_data['hromada'][0]}": max_length_alerts}
        date_start = date_next
    return res_dict


def get_days_with_num_and_length_alerts(data: pd, l_level=('oblast',)) -> dict:
    """
        find the day(s) with the greatest number of the alerts
    """
    res_dict = {}

    date_start = convert_str_to_date(data['started_at'].min(), False)
    date_end = convert_str_to_date(data['started_at'].max(), False)

    data_with_interval_alerts = add_interval_alerts_to_data(data)

    for level in l_level:

        data_by_level = data_with_interval_alerts[data_with_interval_alerts['level'] == level]
        res_dict[level] = get_days_with_num_and_length_alerts_by_level(date_start, date_end, data_by_level)

    return res_dict


def get_max_length_of_alerts(data: pd, l_level=('oblast',)) -> dict:
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


def get_analyze_regions_by_path_month(regions: set, data: pd, level: str) -> dict:
    res_dict = {}
    for region in regions:
        data_by_region = data[data[level] == region]
        if data_by_region.empty:
            continue
        beginning_num_alerts = len(data_by_region[data_by_region['path_of_month'] == 'beginning'])
        middle_num_alerts = len(data_by_region[data_by_region['path_of_month'] == 'middle'])
        end_num_alerts = len(data_by_region[data_by_region['path_of_month'] == 'end'])
        res_dict[region] = {'0_beginning': beginning_num_alerts,
                            '1_middle': middle_num_alerts,
                            '2_end': end_num_alerts}
    return res_dict


def get_analyze_by_month_for_path_month(date_start: datetime, date_end: datetime, data: pd, level: str) -> dict:
    res_dict = {}
    while date_start < date_end:
        date_start_month, date_end_month = get_first_and_last_day_month(date_start)
        date_start = date_end_month + timedelta(days=1)
        temp_data = data[
            (data['started_at'] >= convert_date_to_str(date_start_month)) &
            (data['started_at'] <= convert_date_to_str(date_end_month))]
        regions = set(data.to_dict('list')[level])
        res_dict[(date_start_month, date_end_month)] = get_analyze_regions_by_path_month(regions, temp_data, level)

    return res_dict


def get_analyze_by_path_month(data: pd, l_level=('oblast',)) -> dict:
    """
        analyze which weeks have more alerts the ones that in the beginning of month, in the middle or in the end
    """
    res_dict = {}
    date_start = convert_str_to_date(data['started_at'].min(), False)
    date_end = convert_str_to_date(data['started_at'].max(), False)

    data_with_path_of_month = add_path_of_month(data)

    for level in l_level:

        data_by_level = data_with_path_of_month[data_with_path_of_month['level'] == level]
        res_dict[level] = get_analyze_by_month_for_path_month(date_start, date_end, data_by_level, level)

    return res_dict


def get_region_with_max_alerts(data: pd, l_level=('oblast',)) -> dict:
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


def get_data_for_show_plot(data: pd) -> dict:
    res_dict = {}
    l_region = ('Odeska oblast', 'Zakarpatska oblast', 'Kyiv City', 'Kyivska oblast', 'Kharkivska oblast',
                'Dnipropetrovska oblast')
    get_data = get_analyze_by_week(data)
    get_data = get_data['oblast']

    for region in l_region:
        res_dict[region] = {'day': [], 'num_alerts': [], 'length_alerts': []}
        for key, value in get_data.items():
            if value.get(region):
                res_dict[region]['day'].append(
                    f"{datetime.strftime(key[0], '%d')}-{datetime.strftime(key[1], '%d.%m')}")
                res_dict[region]['num_alerts'].append(value[region]['num alerts'])
                res_dict[region]['length_alerts'].append(value[region]['length alerts'].seconds / 3600)

    return res_dict


def show_plot(data: pd) -> str:
    """
    depict the data of alerts on plot (choose any criteria for depicting you want)

    analyze the alerts condition in your own region
    """

    dict_data = get_data_for_show_plot(data)

    plot_num_alerts = []
    plot_length_alerts = []
    list_region = []

    for region, value in dict_data.items():
        plot_num_alerts.append((value['day'], value['num_alerts']))
        plot_length_alerts.append((value['day'], value['num_alerts']))
        list_region.append(region)

    create_plot(title="Number of alarms", x_label="Date", y_label="Number of alarms per week",
                data_plot=plot_num_alerts, l_legend=list_region, part_save="plot/num_alerts.png")

    create_plot(title="Length of alarms", x_label="Date", y_label="Length of alarms per week, hours",
                data_plot=plot_length_alerts, l_legend=list_region, part_save="plot/length_alerts.png")

    return "Done"


def create_plot(title, x_label, y_label, data_plot, l_legend, part_save, size=(40, 5)) -> None:
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
    except URLError:
        data_pd = pd.read_csv("data_pd.csv")

    dict_funk = {'Analyze by week': get_analyze_by_week(data_pd, ('raion',)),
                 'Analyze by day of week': get_analyze_by_day_of_week(data_pd),
                 'Days with num and length alerts': get_days_with_num_and_length_alerts(data_pd),
                 'Analyze by path month': get_analyze_by_path_month(data_pd),
                 'Region with max alerts': get_region_with_max_alerts(data_pd, ('oblast', 'raion', 'hromada')),
                 'Show plot': show_plot(data_pd)
                 }

    text_to_input = "Choose function: \n"

    for key in dict_funk.keys():
        text_to_input += f"- {key}\n"

    text_to_input += "You'r choose: "

    choosing = True

    while True:
        choosing = input(text_to_input)

        try:
            if choosing == 'Show plot':
                print(dict_funk['Show plot'])
            else:
                pp = pprint.PrettyPrinter()
                pp.pprint(dict_funk[choosing])
        except KeyError:
            break
