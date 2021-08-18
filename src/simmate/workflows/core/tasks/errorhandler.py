# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import os


class ErrorHandler(ABC):
    """
    Abstract base class for an ErrorHandler. These handlers should be used in
    combination with Job and SupervisedJob classes.
    """

    # This class property indicates whether the error handler is a monitor,
    # i.e., a handler that monitors a job as it is running. If a
    # monitor-type handler notices an error, the job will be sent a
    # termination signal, the error is then corrected,
    # and then the job is restarted. This is useful for catching errors
    # that occur early in the run but do not cause immediate failure.
    # Also, is_monitor=True and is_terminating=False is a special case. See the
    # is_terminating description below for why!
    is_monitor = False

    # Whether this handler terminates a job upon error detection. By
    # default, this is True, which means that the current Job will be
    # terminated upon error detection, corrections applied,
    # and restarted. In some instances, some errors may not need the job to be
    # terminated or may need to wait for some other event to terminate a job.
    # For example, a particular error may require a flag to be set to request
    # a job to terminate gracefully once it finishes its current task. The
    # handler to set the flag should be classified as is_terminating = False to
    # not terminate the job.
    is_terminating = True

    # NOTE: if you are using the default check() method (shown below), then you'll
    # need two extra attributes: filename_to_check and possible_error_messages.
    # filename_to_check --> a string of the filename
    # possible_error_messages --> a list of messages to find in the file

    def check(self, directory):
        """
        This method is called during the job (for monitors) or at the end of
        the job to check for errors. It searches for errors and returns the
        error (or list of errors) for correct() method to use. If there are no
        errors, then None (or an empty list) will be returned. In many cases,
        you should read through the files directly rather than use
        calculators.example.outputs which in many cases assumes a completed file.

        As some example, ErrorHandler's can have .check() functions that do one
        of the following:
            (1) returns True when the error is there and False otherwise
            (2) the ErrorHandler includes variations of a particular error, where
                it returns a label such as "Scenario 2" that .correct() can use.
                And in cases where there's no error, either False or None is returned.

        This method can be overwritten, but we have a "default" function below that
        addresses the most common use-case. Here, we have a series of error messages
        and a specific file that they need to be checked in. This default method uses
        self.filename_to_check and self.possible_error_messages to check for an
        error. It then returns True if the errors is found and False otherwise.
        """

        # establish the full path to the output file
        filename = os.path.join(directory, self.filename_to_check)

        # check to see that the file is there first
        if os.path.exists(filename):

            # read the file content and then close it
            with open(filename) as file:
                file_text = file.read()

            # Check if each error is present
            for message in self.possible_error_messages:
                # if the error is NOT present, find() returns a -1
                if file_text.find(message) != -1:
                    # If one of the messages is found, we immediately return that
                    # the error has been found.
                    return True

        # If the file doesn't exist, then we are not seeing any error yet. This line
        # will also be reached if no error was found above.
        return False

    @abstractmethod
    def correct(self, error, directory):
        """
        This method is called at the end of a job when an error is detected.
        It should perform any corrective measures relating to the detected
        error(s). It is given the output from the check() method and based on
        that output, applies a proper fix. It then returns the fix or list
        of fixes made.
        """
        # NOTE TO USER: you will need this line if your function is directory
        # specific and even if not, be sure to include dir (or **kwargs) as
        # input argument for higher-levl compatibility with SupervisedStagedTask
        # dir = get_directory(dir)
        pass

    @property
    def name(self):
        """
        A nice string name for the handler. By default it just returns the name
        of this class.
        """
        return self.__class__.__name__
