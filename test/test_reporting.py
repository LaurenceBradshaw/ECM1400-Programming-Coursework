# Test remove_no_value with list with 0 'No data's and 1 'No data'
# Test add_month with normal date, then one which will need year changing
import pytest
import reporting
import datetime
import main
import utils


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

    @pytest.fixture(autouse=True)
    def change_test_dir(self, request, monkeypatch):
        """
        Change the current working directory for the test so that it looks for and saves data a directory in test/
        """
        monkeypatch.chdir(request.fspath.dirname)

    @pytest.fixture
    def valid_data(self):
        """
        Fixture for valid data
        :return: list of dicts containing valid data
        """
        csv_files = ['test_data_daily.csv', 'test_data_monthly.csv']
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
        def test_expected(self, pollutant, expected, valid_data):
            expected = expected + (['No data']*362)
            actual = reporting.daily_average(valid_data, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestDailyMedian:

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [2.0, 22.05, 19.085]),
            ('pm10', [23.0625, 19.085, 1.25]),
            ('pm25', [20.0, 1.25, 22.05])
        ])
        def test_expected(self, pollutant, expected, valid_data):
            expected = expected + (['No data'] * 362)
            actual = reporting.daily_median(valid_data, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestHourlyAverage:

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [16.5, 14.0625, 16.354166666666668, 14.128333333333336, 12.708333333333334, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0, 1.25, 2.0, 6.0]),
            ('pm10', [16.5, 14.0625, 16.354166666666668, 15.111666666666666, 13.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625, 25.75, 21.125, 23.0625]),
            ('pm25', [16.5, 14.0625, 16.354166666666668, 15.016666666666666, 12.8125, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0, 22.5, 19.0625, 20.0])
        ])
        def test_expected(self, pollutant, expected, valid_data):
            actual = reporting.hourly_average(valid_data, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestMonthlyAverage:

        @pytest.mark.parametrize(['pollutant', 'expected'], [
            ('no', [2.1, 22.1225, 19.6295]),
            ('pm10', [22.1225, 16.69125, 2.1]),
            ('pm25', [19.6295, 1.5625, 22.1225])
        ])
        def test_expected(self, pollutant, expected, valid_data):
            expected = expected + (['No data'] * 9)
            actual = reporting.monthly_average(valid_data, 'test_data_monthly.csv', pollutant)
            assert actual == expected

    class TestPeakHourDate:

        @pytest.mark.parametrize(['date', 'pollutant', 'expected'], [
            (datetime.datetime(year=2021, month=1, day=1), 'no', ('3:00:00', 6.0)),
            (datetime.datetime(year=2021, month=1, day=2), 'pm10', ('1:00:00', 22.5)),
            (datetime.datetime(year=2021, month=1, day=3), 'pm25', ('1:00:00', 25.75))
        ])
        def test_expected(self, date, pollutant, expected, valid_data):
            actual = reporting.peak_hour_date(valid_data, date, 'test_data_daily.csv', pollutant)
            assert actual == expected

    class TestCountMissingData:

        @pytest.mark.parametrize(['pollutant', 'station', 'expected'], [
            ('no', 'test_data_monthly.csv', 4),
            ('pm10', 'test_data_monthly.csv', 3),
            ('pm25', 'test_data_monthly.csv', 1),
            ('no', 'test_data_daily.csv', 0)
        ])
        def test_expected(self, pollutant, station, expected, valid_data):
            actual = reporting.count_missing_data(valid_data, station, pollutant)
            assert actual == expected

    class TestFillMissingData:

        @pytest.mark.parametrize(['pollutant', 'new_value'], [
            ('no', '3.1'),
            ('no', '0.5'),
            ('pm10', '22'),
            ('pm25', '0.90')
        ])
        def test_expected(self, valid_data, pollutant, new_value):
            # count missing data
            missing = reporting.count_missing_data(valid_data, 'test_data_monthly.csv', pollutant)
            # count number of elements with the new value
            data = []
            for d in valid_data['test_data_monthly.csv']:
                data.append(d[pollutant])
            elements_with_new_value = utils.countvalue(data, new_value)
            # fill the missing data
            filled_data = reporting.fill_missing_data(valid_data, new_value, 'test_data_monthly.csv', pollutant)
            # count number of elements with new data
            new_data = []
            for d in filled_data['test_data_monthly.csv']:
                new_data.append(d[pollutant])
            new_count = utils.countvalue(new_data, new_value)
            assert new_count == missing + elements_with_new_value
