import pytest
import monitoring
import main


class TestAddRow:

    @pytest.mark.parametrize(['element', 'column_info', 'wrap', 'col_max', 'expected'], [
        ({'first': "this", 'second': "is a row"}, [("heading", "first"), ("heading2", "second")], 50, {'first': 7, 'second': 8}, "this    | is a row | \n"),
        ({'first': "this", 'second': "is a row that will wrap"}, [("heading", "first"), ("heading2", "second")], 13, {'first': 7, 'second': 23}, "this    | is a row that | \n        | will wrap     | \n")
    ])
    def test_expected(self, element, column_info, wrap, col_max, expected):
        """
        Test that the function returns a correctly formatted row
        :param element: Data to display on the row in the table
        :param column_info: List of tuples containing heading names and dict keys
        :param wrap: Max value a row can be before it wraps on to the next row
        :param col_max: Length of the longest data in each column
        :param expected: Expected row output
        :return: None
        """
        assert monitoring.add_row(element, column_info, wrap, col_max) == expected

    def test_exception_is_raised(self):
        """
        Test that an exception is raised when the data cannot fit on a row
        :return: None
        """
        element = {'first': "this", 'second': "is a row"}
        col_info = [("heading", "first"), ("heading2", "second")]
        wrap = 3
        col_max = {'first': 7, 'second': 8}

        with pytest.raises(Exception):
            monitoring.add_row(element, col_info, wrap, col_max)


class TestMakeTable:

    @pytest.mark.parametrize(['data', 'column_info', 'wrap', 'expected'], [
        ([{'first': "this", 'second': "is a row"}, {'first': "this", 'second': "is a row that will wrap"}], [("heading", "first"), ("heading2", "second")], 13,
         "heading | heading2      |"
         "-------------------------"
         "this    | is a row      | \n"
         "this    | is a row that | \n"
         "        | will wrap     | \n"),
        ([{'first': "this", 'second': "is a row"}, {'first': "this", 'second': "is a row that will wrap"}], [("heading", "first"), ("heading2", "second")], 3,
         "A piece of data contained a segment that was longer than the wrap limit")
    ])
    def test_expected(self, data, column_info, wrap, expected):
        """
        Test that the table which is returned correctly displays the data
        :param data: Data to display in the table
        :param column_info: List of tuples containing heading names and dict keys
        :param wrap: Max value a row can be before it wraps on to the next row
        :param expected: Expected table
        :return: None
        """
        assert monitoring.make_table(data, column_info, wrap)


class TestSave:

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

    @pytest.mark.parametrize(['key', 'filename'], [('test_data_daily.csv', 'test_save_1'), ('test_data_monthly.csv', 'test_save_2')])
    def test_expected(self, valid_data, key, filename):
        """
        Test that the data is saved correctly
        This is done by saving the data, and then reading it back and and comparing it to the original data
        :param valid_data: Test data to save
        :param key: Key for valid_data
        :param filename: Name for file
        :return: None
        """
        monitoring.save(valid_data[key], filename)
        read_back = main.read_file(filename + '.csv')
        for d in read_back:  # Remove the datetime fields that are made when reading the data in because they are removed when saving the data
            del d['datetime']

        assert read_back == valid_data[key]


class TestMakeGraph:

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

    def test_expected(self, valid_data):
        """
        Test that the function returns a graph that represents data as expected
        :param valid_data: Test data
        :return: none
        """
        data = valid_data['test_data_monthly.csv']
        graph = monitoring.make_graph(data, 'no')
        expected_graph = "26.0 +     *             \n" \
                         "     |     *             \n" \
                         "23.5 +     * *      *    \n" \
                         "     |     ****     *    \n" \
                         "21.0 +     ****     * *  \n" \
                         "     |     *****    **** \n" \
                         "18.6 +     *****    *****\n" \
                         "     |     *****    *****\n" \
                         "16.1 +     *****    *****\n" \
                         "     |     *****    *****\n" \
                         "13.6 +     *****    *****\n" \
                         "     |     *****    *****\n" \
                         "11.1 +     *****    *****\n" \
                         "     |     *****    *****\n" \
                         " 8.7 +     *****    *****\n" \
                         "     |     *****    *****\n" \
                         " 6.2 +  *  *****    *****\n" \
                         "     |  *  *****    *****\n" \
                         " 3.7 +  *  *****    *****\n" \
                         "     |***  *****    *****\n" \
                         " 1.2 +**********    *****\n" \
                         "     +-------------------"
        assert graph == expected_graph
