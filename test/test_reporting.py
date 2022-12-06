# Test remove_no_value with list with 0 'No data's and 1 'No data'
# Test add_month with normal date, then one which will need year changing
import pytest
import reporting
import datetime
import main


class TestCustom:

    class TestGetTimeRange:

        @pytest.mark.parametrize(['pollutant', 'start_date', 'end_date', 'expected'], [
            ('no', datetime.datetime(year=2021, month=1, day=1), datetime.datetime(year=2021, month=1, day=3), [7.2, 4.23]),
            ('pm10', datetime.datetime(year=2021, month=1, day=3), datetime.datetime(year=2021, month=1, day=4), [9.2]),
            ('pm25', datetime.datetime(year=2021, month=1, day=5), datetime.datetime(year=2021, month=1, day=7), [])
        ])
        def test_expected(self, pollutant, start_date, end_date, expected):
            data = [
                {'datetime': datetime.datetime(year=2021, month=1, day=1), 'no': 7.2, 'pm10': 3.4, 'pm25': 56.6},
                {'datetime': datetime.datetime(year=2021, month=1, day=2), 'no': 4.23, 'pm10': 0.1, 'pm25': 6.6},
                {'datetime': datetime.datetime(year=2021, month=1, day=3), 'no': 0.2, 'pm10': 9.2, 'pm25': 536.6},
                {'datetime': datetime.datetime(year=2021, month=1, day=4), 'no': 0, 'pm10': 3.23, 'pm25': 9.3}
            ]
            assert reporting.get_time_range(data, start_date, end_date, pollutant) == expected

    class TestAddMonth:

        @pytest.mark.parametrize(['date', 'expected'], [
            (datetime.datetime(year=2021, month=1, day=1), datetime.datetime(year=2021, month=2, day=1)),
            (datetime.datetime(year=2021, month=12, day=1), datetime.datetime(year=2022, month=1, day=1))
        ])
        def test_expected(self, date, expected):
            assert reporting.add_month(date) == expected

    class TestSort:

        @pytest.mark.parametrize(['data', 'expected'], [
            ([4, 6, 3, 7, 5, 3], [3, 3, 4, 5, 6, 7]),
            ([1.2, 3.4, 0.4, 5], [0.4, 1.2, 3.4, 5]),
            ([1, 2, 3], [1, 2, 3]),
            ([], [])
        ])
        def test_expected(self, data, expected):
            assert reporting.sort(data) == expected


class TestTemplate:

    @pytest.fixture
    def valid_data_daily(self):
        """
        Fixture for valid data
        :return: list of dicts containing valid data
        """
        csv_files = ['test_data_daily.csv']
        data = {}
        for file in csv_files:
            data[file] = main.read_file(file)

        return data

    class TestDailyAverage:  # 2.1, 22.1225, 19.6295

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [3.0833333333333335, 22.1225, 19.6295]),
            ('pm10', [23.3125, 19.6295, 2.1]),
            ('pm25', [20.520833333333332, 2.1, 22.1225])
        ])
        def test_expected(self, pollutant, expected, valid_data_daily):
            expected = expected + (['No data']*362)
            actual = reporting.daily_average(valid_data_daily, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestDailyMedian:

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [2.0, 22.05, 19.085]),
            ('pm10', [23.0625, 19.085, 1.25]),
            ('pm25', [20.0, 1.25, 22.05])
        ])
        def test_expected(self, pollutant, expected, valid_data_daily):
            expected = expected + (['No data'] * 362)
            actual = reporting.daily_median(valid_data_daily, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestHourlyAverage:

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [16.5, 14.0625, 16.354166666666668, 14.128333333333336, 12.708333333333334, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0]),
            ('pm10', [16.5, 14.0625, 16.354166666666668, 15.111666666666666, 13.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625]),
            ('pm25', [16.5, 14.0625, 16.354166666666668, 15.016666666666666, 12.8125, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0])
        ])
        def test_expected(self, pollutant, expected, valid_data_daily):
            expected = expected
            actual = reporting.hourly_average(valid_data_daily, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestMonthlyAverage:
        pass

    class TestPeakHourDate:
        pass

    class TestCountMissingData:
        pass

    class TestFillMissingData:
        pass
