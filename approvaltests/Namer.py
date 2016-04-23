import inspect
import os


class Namer(object):
    ClassName = ''
    MethodName = ''
    Directory = ''

    APPROVED = '.approved'
    RECEIVED = '.received'

    def __init__(self, frame=1, extension='.txt'):
        self.extension_with_dot = extension
        self.frame = frame
        self.set_for_stack(inspect.stack(1))

    def get_class_name(self):
        return self.ClassName

    def get_method_name(self):
        return self.MethodName

    def get_directory(self):
        return self.Directory

    def get_basename(self):
        return os.path.join(self.Directory, self.ClassName + "." + self.MethodName)

    def get_received_filename(self, basename=None):
        basename = basename or self.get_basename()
        return basename + self.RECEIVED + self.extension_with_dot

    def get_approved_filename(self, basename=None):
        basename = basename or self.get_basename()
        return basename + self.APPROVED + self.extension_with_dot

    def set_for_stack(self, caller):
        stacktrace = caller[self.frame]
        self.MethodName = stacktrace[3]
        try:
            self.ClassName = stacktrace[0].f_locals["self"].__class__.__name__
        except KeyError:
            # We are inside a function, not a class. Use the name of
            # the function instead of the class name.
            self.ClassName = stacktrace[0].f_code.co_name
            #self.ClassName = ''
        self.Directory = os.path.dirname(stacktrace[1])
