# coding=utf-8
"""Dates util module to build date features as external features."""
import datetime

import numpy as np
import pandas as pd

import holidays_list

DAY = 24
DST_DATES = {
    2000: (datetime.date(2000, 3, 11), datetime.date(2000, 10, 15)),
    2001: (datetime.date(2001, 3, 10), datetime.date(2001, 10, 14)),
    2002: (datetime.date(2002, 3, 9), datetime.date(2002, 10, 13)),
    2003: (datetime.date(2003, 3, 8), datetime.date(2003, 10, 12)),
    2004: (datetime.date(2004, 3, 13), datetime.date(2004, 10, 10)),
    2005: (datetime.date(2005, 3, 12), datetime.date(2005, 10, 9)),
    2006: (datetime.date(2006, 3, 11), datetime.date(2006, 10, 15)),
    2007: (datetime.date(2007, 3, 10), datetime.date(2007, 10, 14)),
    2008: (datetime.date(2008, 3, 29), datetime.date(2008, 10, 12)),
    2009: (datetime.date(2009, 3, 14), datetime.date(2009, 10, 11)),
    2010: (datetime.date(2010, 4, 3), datetime.date(2010, 10, 10)),
    2011: (datetime.date(2011, 5, 7), datetime.date(2011, 8, 21)),
    2012: (datetime.date(2012, 4, 28), datetime.date(2012, 9, 2)),
    2013: (datetime.date(2013, 4, 27), datetime.date(2013, 9, 8)),
    2014: (datetime.date(2014, 4, 26), datetime.date(2014, 9, 7)),
    2015: None,
    2016: (datetime.date(2016, 5, 14), datetime.date(2016, 8, 14)),
    2017: (datetime.date(2017, 5, 13), datetime.date(2017, 8, 13)),
    2018: (datetime.date(2018, 5, 12), datetime.date(2018, 8, 12)),
    2019: (datetime.date(2019, 4, 6), datetime.date(2019, 9, 8)),
    2020: (datetime.date(2020, 4, 4), datetime.date(2020, 9, 6)),
}
COLUMNS = [
    ('DMONTH_1D', 'float64'),
    ('DMONTH_2D', 'float64'),
    ('DDAY_1D', 'float64'),
    ('DDAY_2D', 'float64'),
    ('DHOUR_1D', 'float64'),
    ('DHOUR_2D', 'float64'),
    ('DHOUR_IN_MONTH_1D', 'float64'),
    ('DHOUR_IN_MONTH_2D', 'float64'),
    ('DDAY_OF_WEEK_1D', 'float64'),
    ('DDAY_OF_WEEK_2D', 'float64'),
    ('DDAY_OF_YEAR_1D', 'float64'),
    ('DDAY_OF_YEAR_2D', 'float64'),
    ('DYEAR', 'int16'),
    ('DMONTH', 'int16'),
    ('DDAY', 'int16'),
    ('DHOUR', 'int16'),
    ('DHOUR_IN_MONTH', 'int16'),
    ('DDST_ACTIVE', 'bool'),
    ('DDAY_OF_WEEK', 'int16'),
    ('DDAY_OF_YEAR', 'int16'),
    ('DNONNEGOTIABLE_HOLIDAY', 'bool'),
    ('DCIVIL_HOLIDAY', 'bool'),
    ('DRELIGIOUS_HOLIDAY', 'bool'),
    ('DPEAK_HOUR', 'bool'),
]


class Error(Exception):
    """Errors in this module."""


def _build_holidays_dates(one_holiday):
    """Convert string dat to datetime.date object."""
    one_holiday['fecha'] = datetime.date(
        int(one_holiday['fecha'][:4]), int(one_holiday['fecha'][5:7]),
        int(one_holiday['fecha'][8:]))
    return one_holiday


HOLIDAYS = [
    _build_holidays_dates(one)
    for one in holidays_list.HOLIDAYS if one['nombre'].find('Domingos') == -1
]


def get_2d_representation(value, max_value, min_value=1, grid_size=1000):
    """Convert given value (or values if np array) into a 2D representation."""
    max_min = max_value - min_value + 1
    in_value = 2 * np.pi * (value - min_value) / max_min
    return np.stack([
        grid_size * np.sin(in_value),
        grid_size * np.cos(in_value)]).astype(np.int16).transpose()


def get_is_peak_hour(date, hour):
    """Returns whether given date and hour is within peak hour regulation."""
    # TODO: Implement this!!!
    return 0


def get_2d_date_features(input_array):
    """From general features get final representation.
    Expected row format:
    [year, month, day, hour, hour_in_month, is_dst_active, day_of_week,
     day_of_year, ...]
    """
    month_2d = get_2d_representation(input_array[:, 1], 12)
    day_2d = get_2d_representation(input_array[:, 2], 31)
    hour_2d = get_2d_representation(input_array[:, 3], 24)
    hour_in_month_2d = get_2d_representation(input_array[:, 4], 745)
    day_of_week_2d = get_2d_representation(input_array[:, 6], 6, min_value=0)
    day_of_year_2d = get_2d_representation(input_array[:, 7], 366)
    return np.concatenate([
        month_2d, day_2d, hour_2d, hour_in_month_2d,
        day_of_week_2d, day_of_year_2d, input_array], axis=1)


def get_holiday_and_extra_features(input_array, chilean=True):
    """Complete holiday and other features from date features.
    Expected input_array format:
    [year, month, day, hour, hour_in_month, is_dst_active, ...].
    When chilean flag is False, do not consider holidays
    """
    date_array = [datetime.date(row[0], row[1], row[2]) for row in input_array]
    is_civil_holiday = np.zeros((input_array.shape[0], 1), dtype=np.bool)
    is_religious_holiday = np.zeros((input_array.shape[0], 1), dtype=np.bool)
    is_nonnegotiable_holiday = np.zeros((input_array.shape[0], 1),
                                        dtype=np.bool)
    is_peak_hour = np.zeros((input_array.shape[0], 1), dtype=np.bool)
    day_of_week = -np.ones((input_array.shape[0], 1), dtype=np.int16)
    day_of_year = -np.ones((input_array.shape[0], 1), dtype=np.int16)
    for index, row in enumerate(input_array):
        for one in HOLIDAYS:
            if not chilean:
                continue
            if one['fecha'] == date_array[index]:
                if one['irrenunciable'] == '1':
                    is_nonnegotiable_holiday[index] = 1
                if one['tipo'] == 'Civil':
                    is_civil_holiday[index] = 1
                if one['tipo'] == 'Religioso':
                    is_religious_holiday[index] = 1
        if chilean:
            is_peak_hour[index] = get_is_peak_hour(date_array[index], row[3])
        day_of_week[index] = date_array[index].weekday()
        if day_of_week[index] == 6:
            # Sundays are always Civil holidays
            is_civil_holiday[index] = 1
        day_of_year[index] = date_array[index].toordinal() - datetime.date(
            row[0], 1, 1).toordinal() + 1
    return np.concatenate([
        input_array, day_of_week, day_of_year, is_nonnegotiable_holiday,
        is_civil_holiday, is_religious_holiday, is_peak_hour], axis=1)


def complete_day_hour(year_array, month_array, hour_in_month_array,
                      inverse=False):
    """Complete date info from year, month and hour in month data."""
    dst = [DST_DATES[year] for year in year_array]
    is_dst_active = np.zeros_like(year_array, dtype=np.bool)
    day_array = np.zeros_like(year_array, dtype=np.int16)
    hour_array = np.zeros_like(year_array, dtype=np.int16)
    for index in range(year_array.shape[0]):
        if inverse:
            if dst[index] is None:
                # Assuming non dst time
                is_dst_active[index] = 0
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif (month_array[index] < dst[index][0].month or
                  month_array[index] > dst[index][1].month):
                # Within non dst time
                is_dst_active[index] = 0
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif (dst[index][0].month < month_array[index] <
                  dst[index][1].month):
                # Within dst time
                is_dst_active[index] = 1
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif month_array[index] == dst[index][0].month:
                # Month when dst starts
                hour_of_change = (dst[index][0].day - 1) * DAY
                if hour_in_month_array[index] <= hour_of_change:
                    is_dst_active[index] = 0
                    day_array[index] = (hour_in_month_array[index] -
                                        1) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 1) %
                                         DAY) + 1
                else:
                    is_dst_active[index] = 1
                    day_array[index] = hour_in_month_array[index] // DAY + 1
                    hour_array[index] = (hour_in_month_array[index] % DAY) + 1
            elif month_array[index] == dst[index][1].month:
                # Month when dst ends
                hour_of_change = dst[index][1].day * DAY + 1
                if hour_in_month_array[index] < hour_of_change:
                    is_dst_active[index] = 1
                    day_array[index] = (hour_in_month_array[index] -
                                        1) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 1) %
                                         DAY) + 1
                else:
                    is_dst_active[index] = 0
                    day_array[index] = (hour_in_month_array[index] -
                                        2) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 2) %
                                         DAY) + 1
            else:
                raise Error('Something wrong happened!')
        else:
            if dst[index] is None:
                # Assuming dst time
                is_dst_active[index] = 1
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif (month_array[index] < dst[index][0].month or
                  month_array[index] > dst[index][1].month):
                # Within dst time
                is_dst_active[index] = 1
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif (dst[index][0].month < month_array[index] <
                  dst[index][1].month):
                # Within non dst time
                is_dst_active[index] = 0
                day_array[index] = (hour_in_month_array[index] - 1) // DAY + 1
                hour_array[index] = ((hour_in_month_array[index] - 1) %
                                     DAY) + 1
            elif month_array[index] == dst[index][0].month:
                # Month when dst ends
                hour_of_change = dst[index][0].day * DAY
                if hour_in_month_array[index] <= hour_of_change:
                    is_dst_active[index] = 1
                    day_array[index] = (hour_in_month_array[index] -
                                        1) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 1) %
                                         DAY) + 1
                else:
                    is_dst_active[index] = 0
                    day_array[index] = (hour_in_month_array[index] -
                                        2) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 2) %
                                         DAY) + 1
            elif month_array[index] == dst[index][1].month:
                # Month when dst starts
                hour_of_change = (dst[index][1].day - 1) * DAY + 1
                if hour_in_month_array[index] < hour_of_change:
                    is_dst_active[index] = 0
                    day_array[index] = (hour_in_month_array[index] -
                                        1) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 1) %
                                         DAY) + 1
                elif hour_in_month_array[index] > hour_of_change:
                    is_dst_active[index] = 1
                    day_array[index] = (hour_in_month_array[index] -
                                        1) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index] - 1) %
                                         DAY) + 1
                else:
                    # This hour is set equal to the next, as it is a changing
                    # time hour. All its data should be 0 (check that!). This
                    # is fixed in the input array
                    is_dst_active[index] = 1
                    day_array[index] = (hour_in_month_array[index]) // DAY + 1
                    hour_array[index] = ((hour_in_month_array[index]) %
                                         DAY) + 1
                    # Next line is important to avoid having the same hour
                    # annotated with different hour in month
                    hour_in_month_array[index] += 1
            else:
                raise Error('Something wrong happened!')
    return np.stack([year_array, month_array, day_array, hour_array,
                     hour_in_month_array, is_dst_active]).transpose()


def complete_hour_in_month(year_array, month_array, day_array, hour_array,
                           chilean=True):
    """Complete date info from year, month and hour in month data.
    When chilean is False, do not consider DST.
    """
    dst = [DST_DATES[year] for year in year_array]
    is_dst_active = np.zeros_like(year_array, dtype=np.bool)
    hour_in_month_array = np.zeros_like(year_array, dtype=np.int16)
    for index in range(year_array.shape[0]):
        if not chilean:
            # DST is not considered, assuming equal to "Chilean winter time"
            is_dst_active[index] = 0
            hour_in_month_array[index] = (hour_array[index] +
                                          (day_array[index] - 1) * DAY)
        elif dst[index] is None:
            # Assuming dst time
            is_dst_active[index] = 1
            hour_in_month_array[index] = (hour_array[index] +
                                          (day_array[index] - 1) * DAY)
        elif (month_array[index] < dst[index][0].month or
              month_array[index] > dst[index][1].month):
            # Within dst time
            is_dst_active[index] = 1
            hour_in_month_array[index] = (hour_array[index] +
                                          (day_array[index] - 1) * DAY)
        elif dst[index][0].month < month_array[index] < dst[index][1].month:
            # Within non dst time
            is_dst_active[index] = 0
            hour_in_month_array[index] = (hour_array[index] +
                                          (day_array[index] - 1) * DAY)
        elif month_array[index] == dst[index][0].month:
            # Month when dst ends
            if day_array[index] < dst[index][0].day:
                # Within dst time
                is_dst_active[index] = 1
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
            elif day_array[index] > dst[index][0].day:
                # Within non dst time
                is_dst_active[index] = 0
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY + 1)
            elif hour_array[index] <= DAY:
                is_dst_active[index] = 1
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
            else:
                # Mark hour as 25 in input files please !
                is_dst_active[index] = 0
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
                # Fixing hour to be 24 with dst off, instead of 25
                hour_array[index] = 24
        elif month_array[index] == dst[index][1].month:
            # Month when dst starts
            if day_array[index] < dst[index][1].day:
                is_dst_active[index] = 0
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
            elif day_array[index] > dst[index][1].day:
                is_dst_active[index] = 1
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
            elif hour_array[index] > 1:
                is_dst_active[index] = 1
                hour_in_month_array[index] = (hour_array[index] +
                                              (day_array[index] - 1) * DAY)
            else:
                # Changing time day, hour 1. They have value 0 in files,
                # so it is marked as following hour
                is_dst_active[index] = 1
                hour_in_month_array[index] = (hour_array[index] + 1 +
                                              (day_array[index] - 1) * DAY)
                hour_array[index] = 2
    return np.stack([year_array, month_array, day_array, hour_array,
                     hour_in_month_array, is_dst_active]).transpose()


def get_complete_date_features(year_array, month_array, day_array=None,
                               hour_array=None, hour_in_month_array=None,
                               chilean=True, inverse=False):
    """Complete date features from input data.
    Year and month are always given. Either day and hour are given,
    or the hour within the month.
    When chilean flag is False, do not consider holidays or DST (except to
        complete hour from hour_in_month).
    When inverse flag is True, DST dates are interpreted as mid year is DST.
    """
    year_array = np.array([int(value) for value in year_array], dtype=np.int16)
    month_array = np.array([int(value) for value in month_array],
                           dtype=np.int16)
    if hour_in_month_array is None:
        day_array = np.array([int(value) for value in day_array],
                             dtype=np.int16)
        hour_array = np.array([int(value) for value in hour_array],
                              dtype=np.int16)
        base_array = complete_hour_in_month(year_array, month_array, day_array,
                                            hour_array, chilean=chilean)
    else:
        hour_in_month_array = np.array(
            [int(value) for value in hour_in_month_array], dtype=np.int16)
        base_array = complete_day_hour(year_array, month_array,
                                       hour_in_month_array, inverse=inverse)
    base_array = get_holiday_and_extra_features(base_array, chilean=chilean)
    data_frame = pd.DataFrame(data=get_2d_date_features(base_array),
                              columns=[col_name for col_name, _ in COLUMNS])
    for col_name, col_dtype in COLUMNS:
        if col_dtype != 'float64':
            data_frame[col_name] = data_frame[col_name].astype(col_dtype)
    return data_frame
