# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tools for dealing with eventually consistent tests.
"""

from retrying import retry


def _retry_on_exception(exception_class):
    def inner(e):
        if isinstance(e, exception_class):
            print('Retrying due to eventual consistency.')
            return True
        return False


def mark(f):
    """Marks an entire test as eventually consistent and retries."""
    __tracebackhide__ = True
    return retry(
        wait_exponential_multiplier=100,
        wait_exponential_max=1500,
        stop_max_attempt_number=5,
        retry_on_exception=_retry_on_exception(AssertionError))(f)


def call(f, exceptions=AssertionError, tries=4):
    """Call a given function and treat it as eventually consistent.

    The function will be called immediately and retried with exponential
    backoff up to the listed amount of times.

    By default, it only retries on AssertionErrors, but can be told to retry
    on other errors.

    For example:

        @eventually_consistent.call
        def _():
            results = client.query().fetch(10)
            assert len(results) == 10

    """
    __tracebackhide__ = True
    return retry(
        wait_exponential_multiplier=100,
        wait_exponential_max=1000,
        stop_max_attempt_number=tries,
        retry_on_exception=_retry_on_exception(exceptions))(f)()
