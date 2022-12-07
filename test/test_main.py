import datetime

import pytest
import main
import reporting


class TestCustom:

    class TestReadFile:

        @pytest.fixture
        def valid_file_data(self):
            """
            Fixture for valid data
            :return: list of dicts containing valid data
            """
            return main.read_file("Pollution-London Harlington.csv")

        @pytest.mark.parametrize(["f_name", "output_type"], [
            ("Pollution-London Harlington.csv", list),
            ("This file does not exist.csv", type(None))
        ])
        def test_output_types(self, f_name, output_type):
            """
            Test the function returns the correct types when given valid and invalid file names
            :return: None
            """
            data = main.read_file(f_name)
            assert type(data) is output_type

        def test_expected_dimensions(self, valid_file_data):
            """
            Test the function returns a list with the expected dimensions
            :return: None
            """
            days = 365
            hours = 24
            total_entries = days * hours
            assert len(valid_file_data) == total_entries

        def test_list_of_dicts(self, valid_file_data):
            """
            Test the valid data is a list of dicts
            :return: None
            """
            is_dict = [True if type(element) == dict else False for element in valid_file_data]
            assert all(is_dict)

        @pytest.mark.parametrize("dict_key", ['date', 'time', 'no', 'pm10', 'pm25'])
        def test_expected_dict_keys(self, valid_file_data, dict_key):
            """
            Test the first element in the list is a dictionary with the expected keys
            :return: None
            """
            keys = list(valid_file_data[0].keys())

            assert dict_key in keys

        class TestGetDailyDates:

            @pytest.mark.parametrize('date', [
                (datetime.datetime(year=2021, month=1, day=1)),
                (datetime.datetime(year=2021, month=1, day=2)),
                (datetime.datetime(year=2021, month=2, day=1)),
                (datetime.datetime(year=2022, month=1, day=1))
            ])
            def test_dates_are_a_day_apart(self, date):
                dates = main.get_daily_dates(date)
                assert len(dates) == 365

                day_apart = []
                for i in range(1, len(dates)):
                    if datetime.datetime.strptime(dates[i], '%Y-%m-%d') - datetime.datetime.strptime(dates[i - 1], '%Y-%m-%d') == datetime.timedelta(days=1):
                        day_apart.append(True)
                    else:
                        day_apart.append(False)

                assert all(day_apart)

        class TestGetHourlyTimes:

            def test_expected(self):
                assert main.get_hourly_times() == ['1:00:00', '2:00:00', '3:00:00', '4:00:00', '5:00:00', '6:00:00', '7:00:00', '8:00:00',
                                                   '9:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00',
                                                   '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00', '24:00:00']

        class TestGetMonthlyDates:

            @pytest.mark.parametrize('date', [
                (datetime.datetime(year=2021, month=1, day=1)),
                (datetime.datetime(year=2021, month=1, day=2)),
                (datetime.datetime(year=2021, month=2, day=1)),
                (datetime.datetime(year=2021, month=12, day=1))
            ])
            def test_dates_are_a_month_apart(self, date):
                actual = main.get_monthly_dates(date)

                month_apart = []

                for i in range(1, len(actual)):
                    datetime_date = datetime.datetime.strptime(actual[i], '%Y-%m-%d')
                    prev_datetime_date = datetime.datetime.strptime(actual[i - 1], '%Y-%m-%d')
                    if reporting.add_month(prev_datetime_date) == datetime_date:
                        month_apart.append(True)
                    else:
                        month_apart.append(False)

                assert all(month_apart)
