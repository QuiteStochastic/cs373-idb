
from io import StringIO
import sys
import traceback
import unittest

class JsonTestResult(unittest.TextTestResult):
    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1):
        unittest.TextTestResult.__init__(self, stream, descriptions, verbosity)
        self.result_obj = {'success':0,
                           'failure':0,
                           'error':0,
                           'expectedFailure':0,
                           'unexpectedSuccess':0,
                           'total':0,
                           'results':[]}
    
    def appendResult(self, test, status, **kwargs):
        r = {'name':test._testMethodName, 'status':status}
        for k, v in kwargs.items():
            r[k]=v
        self.result_obj['results'].append(r)
        
        if(status == 'success'):
            self.result_obj['success'] += 1
        elif(status == 'failed'):
            self.result_obj['failure'] += 1
        elif(status == 'error'):
            self.result_obj['error'] += 1
        elif(status == 'expected failure'):
            self.result_obj['expectedFailure'] += 1
        elif(status == 'unexpected success'):
            self.result_obj['unexpectedSuccess'] += 1
        self.result_obj['total'] += 1
    
    def addSuccess(self, test):
        unittest.TextTestResult.addSuccess(self, test)
        self.appendResult(test, 'success')
    
    def addFailure(self, test, reason):
        unittest.TextTestResult.addFailure(self, test, reason)
        self.appendResult(test, 'failed', reason=reason[1].args[0],
                          traceback=traceback.format_tb(reason[2]))
    
    def addError(self, test, reason):
        unittest.TextTestResult.addError(self, test, reason)
        self.appendResult(test, 'error', reason=reason[1].args[0],
                          traceback=traceback.format_tb(reason[2]))
    
    def addSkip(self, test, reason):
        unittest.TextTestResult.addSkip(self, test, reason)
        self.appendResult(test, 'skip', reason=reason)
    
    def addExpectedFailure(self, test, reason):
        unittest.TextTestResult.addExpectedFailure(self, test, reason)
        self.appendResult(test, 'expected failure', reason=reason[1].args[0],
                          traceback=traceback.format_tb(reason[2]))
    
    def addUnexpectedSuccess(self, test):
        unittest.TextTestResult.addUnexpectedSuccess(self, test)
        self.appendResult(test, 'unexpected success')

class JsonWriter(object):
    def __init__(self, stream, compressed=True, indent='  '):
        self.stream = stream
        self.compressed = compressed
        self.indent = indent
    
    def write(self, json_obj):
        if(self.compressed):
            self.stream.write(str(json_obj))
        else:
            self._write_impl(json_obj)
        self.stream.write('\n')
    
    def _write_impl(self, jobject, indentation="", continuation=False):
        nindent = indentation + self.indent
        if(type(jobject) == dict):
            if(not continuation):
                self.stream.write(indentation)
            self.stream.write('{\n')
            for k, v in jobject.items():
                self.stream.write(nindent + '"' + k + '": ');
                self._write_impl(v, nindent, True)
                self.stream.write(',\n')
            self.stream.write(indentation + '}')
        elif(type(jobject) == list):
            if(not continuation):
                self.stream.write(indentation)
            self.stream.write('[\n')
            for i in jobject:
                self._write_impl(i, nindent)
                self.stream.write(',\n')
            self.stream.write(indentation + ']')
        elif(type(jobject) == str):
            if(not continuation):
                self.stream.write(indentation)
            self.stream.write(repr(jobject))
        else:
            if(not continuation):
                self.stream.write(indentation)
            self.stream.write(str(jobject))

class JsonTestRunner(unittest.TextTestRunner):
    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1,
                 printJSON=True, compressed=False):
        self.resultstream = stream
        self.compressed = compressed
        txtstream = stream
        self.printJSON = printJSON
        if self.printJSON:
            txtstream = StringIO()
        unittest.TextTestRunner.__init__(self, txtstream, descriptions,
                                         verbosity)
    
    def run(self, test):
        r = unittest.TextTestRunner.run(self, test)
        self.result = r
        if self.printJSON:
            writer = JsonWriter(self.resultstream, self.compressed)
            writer.write(r.result_obj)
        return r
    
    def _makeResult(self):
        return JsonTestResult(self.stream, self.descriptions, self.verbosity)
