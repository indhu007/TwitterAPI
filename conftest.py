from datetime import datetime
import logging

log = logging.getLogger(__name__)

# def pytest_assertrepr_compare(op, left, right):
#     """ This function will print log everytime the assert fails"""
#     log.error('Comparing Foo instances:    vals: %s != %s \n' % (left, right))
#     return ["Comparing Foo instances:", " vals: %s != %s" % (left, right)]

def pytest_configure(config):
    """ Create a log file if log_file is not mentioned in *.ini file"""
    if not config.option.log_file:
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
        config.option.log_file = 'log.' + timestamp