import ibm_db
conn = ibm_db.connect("AUTHENTICATION=SERVER;DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tmj80232;PWD=XFJsY2e4yqV8KpXS",'','')
print(conn)
print("connection successful...")
