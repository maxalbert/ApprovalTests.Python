from approvaltests.ApprovalException import ApprovalException
from approvaltests.FileApprover import FileApprover
from approvaltests.Namer import Namer
from approvaltests.ReceivedFileLauncherReporter import ReceivedFileLauncherReporter
from approvaltests.StringWriter import StringWriter


def verify(data, reporter=ReceivedFileLauncherReporter(), methodname=None):
    approver = FileApprover()
    namer = Namer(2, methodname=methodname)
    writer = StringWriter(data)

    error = approver.verify(namer, writer, reporter)
    if error is not None:
        raise ApprovalException(error)
