import sys
sys.path.insert(0, '/home/jovyan')


from dsflow.helpers import DsflowContext


# Initialize dsflow and spark
(dsflow, spark) = DsflowContext.create()
