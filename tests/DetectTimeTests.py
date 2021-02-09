import datetime
import timeit
import uuid
from unittest import TestCase, mock
from plan_monitor import config
from plan_monitor.detect import find_bad_plans

def get_time_diff_from_ms(start_time: datetime, seconds_to_subtract: int) -> int:
    ts = start_time - datetime.timedelta(seconds=seconds_to_subtract)
    return ts.timestamp() * 1000

def generate_plan_payload(numberToCreate, stats_time):
    plans = {}
    duplicate_query_plan_hash = '234242342'
    query_handle = '253252342'
    for i in range(0, numberToCreate):
        plan_value = uuid.uuid4()
        plans[plan_value] ={
            "creation_time": 234234242,
            "last_execution_time": 2342342,
            "worst_statement_query_plan_hash": duplicate_query_plan_hash,
            "execution_count": 23,
            "total_elapsed_time": 90,
            "total_logical_reads": 98,
            "total_logical_writes": 0,
            "statement_count": 1,
            "worst_statement_query_hash": "324342",
            "worst_statement_start_offset": "2342342",
            "sql_handle": query_handle,
            "db_identifier": '23423',
            "stats_query_time" : stats_time
        }
    return plans


class FindBadPlans(TestCase):

    @mock.patch('plan_monitor.config')
    def test_time_to_find_bad_plans(self, conf):
        conf.MAX_AGE_OF_LAST_EXECUTION_SECONDS.return_value = 5
        conf.MAX_NEW_PLAN_AGE_SECONDS.return_value = 3
        dt = datetime.datetime.now()
        stats_time = dt.timestamp() * 1000
        duplicate_query_plan_hash = '3r23423424'
        query_handle = '2342342'
        plans = {
            'plan-one-duplicate-qp-hash-not-established': {
                "creation_time": 234234242,
                "last_execution_time": 2342342,
                "worst_statement_query_plan_hash": duplicate_query_plan_hash,
                "execution_count": 23,
                "total_elapsed_time": 90,
                "total_logical_reads": 98,
                "total_logical_writes": 0,
                "statement_count": 1,
                "worst_statement_query_hash": "324342",
                "worst_statement_start_offset": "2342342",
                "sql_handle": query_handle,
                "db_identifier": '23423',
                "stats_query_time" : stats_time
            },
            'not-a-match-established': {
                "creation_time":  2352523,
                "last_execution_time": 345345356,
                "worst_statement_query_plan_hash": "not-a-query-plan-hash-match",
                "execution_count": 23,
                "total_elapsed_time": 90,
                "total_logical_reads": 98,
                "total_logical_writes": 0,
                "statement_count": 1,
                "worst_statement_query_hash": "324342",
                "worst_statement_start_offset": "2342342",
                "sql_handle": query_handle,
                "db_identifier": '23423',
                "stats_query_time" : stats_time
            },
            'plan-two-duplicate-qp-hash-is-established': {
                "creation_time": 235235363,
                "last_execution_time": 35253574,
                "worst_statement_query_plan_hash": duplicate_query_plan_hash,
                "execution_count": 23,
                "total_elapsed_time": 90,
                "total_logical_reads": 98,
                "total_logical_writes": 0,
                "statement_count": 1,
                "worst_statement_query_hash": "324342",
                "worst_statement_start_offset": "2342342",
                "sql_handle": query_handle,
                "db_identifier": '23423',
                "stats_query_time" : stats_time
            }
        }
        generate_plan_payload(34, stats_time)
        setup = '''
from plan_monitor.detect import find_bad_plans
import datetime
import uuid
dt = datetime.datetime.now()
stats_time = dt.timestamp() * 1000
duplicate_query_plan_hash = '3r23423424'
query_handle = '2342342'
def generate_plan_payload(numberToCreate, stats_time):
    plans = {}
    duplicate_query_plan_hash = '234242342'
    query_handle = '253252342'
    for i in range(0, numberToCreate):
        plan_value = uuid.uuid4()
        plans[plan_value] ={
            "creation_time": 234234242,
            "last_execution_time": 2342342,
            "worst_statement_query_plan_hash": duplicate_query_plan_hash,
            "execution_count": 23,
            "total_elapsed_time": 90,
            "total_logical_reads": 98,
            "total_logical_writes": 0,
            "statement_count": 1,
            "worst_statement_query_hash": "324342",
            "worst_statement_start_offset": "2342342",
            "sql_handle": query_handle,
            "db_identifier": '23423',
            "stats_query_time" : stats_time
        }
    return plans
    
plans = generate_plan_payload(800, stats_time)'''
        find_bad_plans(plans, 3232352)
        timed_stuff = timeit.timeit(setup=setup, stmt='find_bad_plans(plans, stats_time)', number=1000)
        print(timed_stuff)
        self.assertTrue(False)