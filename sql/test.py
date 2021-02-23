import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:169.254.208.1' 
database = 'DemoDB2' 
username = 'master' 
password = 'control' 
# DATABASE='+database+';
cnxn = pyodbc.connect('DRIVER=FreeTDS;DNS=HomeSQL;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()