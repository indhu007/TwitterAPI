from datetime import datetime
import logging

import pytest

from Utils.email_pytest_report import Email_Pytest_Report

log = logging.getLogger(__name__)

@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    return request.config.getoption("--email_pytest_report")


def pytest_addoption(parser):
    parser.addoption("--email_pytest_report", dest="email_pytest_report", help="Email pytest report: Y or N",
                     default="N")


def pytest_terminal_summary(terminalreporter, exitstatus):
    "add additional section in terminal summary reporting."
    if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
        # Initialize the Email_Pytest_Report object
        email_obj = Email_Pytest_Report()
        # Send html formatted email body message with pytest report as an attachment
        email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path='default')

# def pytest_assertrepr_compare(op, left, right):
#     """ This function will print log everytime the assert fails"""
#     log.error('Comparing Foo instances:    vals: %s != %s \n' % (left, right))
#     return ["Comparing Foo instances:", " vals: %s != %s" % (left, right)]

def pytest_configure(config):
    """ Create a log file if log_file is not mentioned in *.ini file"""
    if not config.option.log_file:
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
        config.option.log_file = 'log.' + timestamp