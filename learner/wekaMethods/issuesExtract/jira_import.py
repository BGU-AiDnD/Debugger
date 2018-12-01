__author__ = 'amir'

import jira
import csv
import unicodedata
import datetime
import utilsConf

#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue):
    def to_string(s):
        return str( unicodedata.normalize('NFKD', s).encode('ascii','ignore'))
    Id=issue.key.split("-")[1]
    Product=str(issue.fields.project)
    Component=",".join([x.name for x in issue.fields.components])
    Assigned_To="NONE"
    if issue.fields.assignee!=None:
        Assigned_To= to_string(issue.fields.assignee.name)
    Status=str(issue.fields.status)
    Resolution=str(issue.fields.resolution)
    Reporter = ""
    if issue.fields.reporter is not None:
        Reporter = to_string(issue.fields.reporter.name)
    Last_Modified=str(issue.fields.updated)[:10]
    Last_Modified=datetime.datetime.strptime(Last_Modified,'%Y-%m-%d').date().strftime('%d/%m/%Y %H:%M:%S')

    Version = ""
    if hasattr(issue.fields, 'versions'):
        Version=",".join([v.name for v in getattr(issue.fields, 'versions')])
    Milestone=",".join([v.name for v in issue.fields.fixVersions])
    Hardware=str("")
    OS=""
    if not None==issue.fields.environment:
        OS=to_string(issue.fields.environment)
        OS=" ".join(OS.split())
    Priority=str("")
    if "priority" in  issue.raw:
        Priority=str("P"+issue.raw["priority"]["id"])
    Severity=str("")
    if "issuetype"  in  issue.raw:
        Severity=str(issue.raw["issuetype"]["name"])
    Summary=to_string(issue.fields.summary)
    Summary=Summary.replace("\n"," ")
    Keywords=str(issue.fields.labels)
    Submit_Date=str(issue.fields.created)[:10]
    Submit_Date=datetime.datetime.strptime(Submit_Date,'%Y-%m-%d').date().strftime('%d/%m/%Y %H:%M:%S')
    Blocks=str("")
    Depends_On=str("")
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=str("")
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]

# @utilsConf.marker_decorator(utilsConf.ISSUE_TRACKER_FILE)
def jiraIssues(outFile , url, project_name, bunch = 100):
    jiraE = jira.JIRA(url)
    allIssues=[]
    extracted_issues = 0
    lines = [
        ["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version",
         "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time",
         "blocks", "depends_on", "Duplicate Of", "cc"]]
    while True:
        issues = jiraE.search_issues("project={0}".format(project_name), maxResults=bunch, startAt=extracted_issues)
        allIssues.extend(issues)
        extracted_issues = extracted_issues+bunch
        if len(issues) < bunch:
            break
    for issue in allIssues:
        if issue.fields.issuetype.name.lower() != 'bug':
            continue
        analyze = issueAnalyze(issue)
        lines.append(analyze)
    with open(outFile,"wb") as f:
        writer=csv.writer(f)
        writer.writerows(lines)

if __name__ == "__main__":
    # jiraIssues("C:\\temp\\CASSANDRA2.csv", "https://issues.apache.org/jira",'CASSANDRA')
    all_apache_projects = [u'AGILA', u'AAR', u'ABDERA', u'ACCUMULO', u'ACE', u'ACL', u'AMQ', u'AMQNET', u'APLO', u'ARTEMIS', u'AMQCPP', u'AMQCLI', u'OPENWIRE', u'BLAZE', u'ADDR', u'AIRAVATA', u'ALOIS', u'ARMI', u'AMBARI', u'AMBER', u'ANAKIA', u'ANNO', u'AIRFLOW', u'ANY23', u'APEXCORE', u'APEXMALHAR', u'ARROW', u'ASTERIXDB', u'AWF', u'BLUR', u'CMDA', u'COMMONSRDF', u'CONCERTED', u'CB', u'CURATOR', u'DIRECTMEMORY', u'DRILL', u'FINERACT', u'FLEX', u'FREEMARKER', u'GEARPUMP', u'GOBBLIN', u'GORA', u'HAWQ', u'HELIX', u'HORN', u'JENA', u'KNOX', u'LENS', u'CLOWNFISH', u'MADLIB', u'MASFRES', u'METAMODEL', u'NIFI', u'MINIFI', u'OLTU', u'OMID', u'ONAMI', u'CLIMATE', u'OPENAZ', u'QPIDIT', u'QUICKSTEP', u'RAT', u'RIPPLE', u'ROCKETMQ', u'ROL', u'S4', u'STORM', u'TAVERNA', u'TENTACLES', u'TEZ', u'MTOMCAT', u'TRAFODION', u'TWILL', u'UNOMI', u'WHIRR', u'WHISKER', u'APACHECON', u'MRM', u'ARIA', u'ARIES', u'ASYNCWEB', u'ATLAS', u'ATTIC', u'AURORA', u'AVALON', u'AVNSHARP', u'RUNTIME', u'STUDIO', u'CENTRAL', u'PLANET', u'TOOLS', u'PNIX', u'AVRO', u'AXIOM', u'AXIS', u'AXISCPP', u'WSIF', u'AXIS2', u'TRANSPORTS', u'AXIS2C', u'BAHIR', u'BATCHEE', u'BATIK', u'BEAM', u'BEEHIVE', u'BIGTOP', u'BLUESKY', u'BOOKKEEPER', u'TM', u'BROOKLYN', u'BUILDR', u'BVAL', u'STDCXX', u'CACTUS', u'CALCITE', u'CAMEL', u'CARBONDATA', u'CASSANDRA', u'CAY', u'CELIX', u'CMIS', u'CHUKWA', u'CLEREZZA', u'CLK', u'CLKE', u'CLOUDSTACK', u'COCOON', u'COCOON3', u'COMMONSSITE', u'ATTRIBUTES', u'BCEL', u'BEANUTILS', u'BETWIXT', u'BSF', u'CHAIN', u'CLI', u'CODEC', u'COLLECTIONS', u'COMPRESS', u'CONFIGURATION', u'CRYPTO', u'CSV', u'DAEMON', u'DBCP', u'DBUTILS', u'DIGESTER', u'DISCOVERY', u'DORMANT', u'EL', u'EMAIL', u'EXEC', u'FEEDPARSER', u'FILEUPLOAD', u'FUNCTOR', u'IMAGING', u'IO', u'JCI', u'JCS', u'JELLY', u'JEXL', u'JXPATH', u'LANG', u'LAUNCHER', u'LOGGING', u'MATH', u'MODELER', u'NET', u'NUMBERS', u'OGNL', u'POOL', u'PRIMITIVES', u'PROXY', u'RESOURCES', u'RNG', u'SANDBOX', u'SANSELAN', u'SCXML', u'TEXT', u'TRANSACTION', u'VALIDATOR', u'VFS', u'WEAVER', u'COMDEV', u'CONTINUUM', u'COR', u'COTTON', u'COUCHDB', u'CRUNCH', u'CTAKES', u'CXF', u'DOSGI', u'CXFXJC', u'FEDIZ', u'DATAFU', u'DAYTRADER', u'DDLUTILS', u'DTACLOUD', u'DELTASPIKE', u'DEPOT', u'DERBY', u'DMAP', u'DIR', u'DIRSERVER', u'DIRAPI', u'DIRGROOVY', u'DIRKRB', u'DIRNAMING', u'DIRSHARED', u'DIRSTUDIO', u'DL', u'DBF', u'DROIDS', u'DVSL', u'EAGLE', u'EASYANT', u'ECS', u'EDGENT', u'EMPIREDB', u'ESME', u'ESCIMO', u'ETCH', u'EWS', u'EXLBR', u'FORTRESS', u'FALCON', u'FELIX', u'FLINK', u'FLUME', u'FOP', u'FOR', u'FC', u'FTPSERVER', u'GBUILD', u'GEODE', u'GERONIMO', u'GERONIMODEVTOOLS', u'GIRAPH', u'GOSSIP', u'GRFT', u'GRIFFIN', u'GROOVY', u'GSHELL', u'GUACAMOLE', u'GUMP', u'HADOOP', u'HDT', u'HDFS', u'MAPREDUCE', u'YARN', u'HAMA', u'HARMONY', u'HBASE', u'HCATALOG', u'HERALDRY', u'HISE', u'HIVE', u'HIVEMALL', u'HIVEMIND', u'HTRACE', u'HTTPASYNC', u'HTTPCLIENT', u'HTTPCORE', u'IBATISNET', u'IBATIS', u'RBATIS', u'IGNITE', u'IMPALA', u'IMPERIUS', u'INCUBATOR', u'INFRATEST', u'INFRA', u'INFRAP', u'IOTA', u'ISIS', u'IVY', u'IVYDE', u'JCR', u'JCRVLT', u'JCRBENCH', u'JCRCL', u'JCRSERVLET', u'JCRTCK', u'JCRRMI', u'OAK', u'OCM', u'JCRSITE', u'HUPA', u'IMAP', u'JDKIM', u'JSIEVE', u'JSPF', u'MAILBOX', u'MAILET', u'MIME4J', u'MPT', u'POSTAGE', u'PROTOCOLS', u'JAMES', u'JAXME', u'JCLOUDS', u'JDO', u'JS1', u'JS2', u'JOHNZON', u'JOSHUA', u'JSEC', u'JSPWIKI', u'JUDDI', u'JUNEAU', u'KAFKA', u'KALUMET', u'KAND', u'KARAF', u'KATO', u'KI', u'KITTY', u'KUDU', u'KYLIN', u'LABS', u'HTTPDRAFT', u'LEGAL', u'LIBCLOUD', u'LOGCXX', u'LOG4J2', u'LOG4NET', u'LOG4PHP', u'LOKAHI', u'LUCENE', u'LUCENENET', u'LCN4C', u'LUCY', u'MAHOUT', u'CONNECTORS', u'MARMOTTA', u'MNG', u'MACR', u'MANT', u'MANTTASKS', u'MANTRUN', u'ARCHETYPE', u'MARCHETYPES', u'MASSEMBLY', u'MCHANGELOG', u'MCHANGES', u'MCHECKSTYLE', u'MCLEAN', u'MCOMPILER', u'MDEP', u'MDEPLOY', u'MDOAP', u'MDOCCK', u'DOXIA', u'DOXIASITETOOLS', u'DOXIATOOLS', u'MEAR', u'MECLIPSE', u'MEJB', u'MENFORCER', u'MGPG', u'MPH', u'MINDEXER', u'MINSTALL', u'MINVOKER', u'MJAR', u'MJARSIGNER', u'MJAVADOC', u'JXR', u'MLINKCHECK', u'MPATCH', u'MPDF', u'MPLUGINTESTING', u'MPLUGIN', u'MPMD', u'MPOM', u'MPIR', u'MNGSITE', u'MRAR', u'MRELEASE', u'MRRESOURCES', u'MREPOSITORY', u'MRESOLVER', u'MRESOURCES', u'SCM', u'MSCMPUB', u'MSHADE', u'MSHARED', u'MSITE', u'MSKINS', u'MSOURCES', u'MSTAGE', u'SUREFIRE', u'MTOOLCHAINS', u'MVERIFIER', u'WAGON', u'MWAR', u'MAVIBOT', u'MEECROWAVE', u'MESOS', u'METRON', u'MILAGRO', u'DIRMINA', u'SSHD', u'MIRAE', u'MJDEPS', u'MNEMONIC', u'MODPYTHON', u'MRQL', u'MRUNIT', u'MUSE', u'ADFFACES', u'EXTCDI', u'MFCOMMONS', u'MYFACES', u'EXTSCRIPT', u'EXTVAL', u'MFHTML5', u'ORCHESTRA', u'PORTLETBRIDGE', u'MYFACESTEST', u'TOBAGO', u'TOMAHAWK', u'TRINIDAD', u'MYNEWT', u'MYNEWTDOC', u'MYRIAD', u'NEETHI', u'NETBEANS', u'NIFIREG', u'NPANDAY', u'NUTCH', u'NUVEM', u'ODE', u'JACOB', u'OWC', u'ODFTOOLKIT', u'OFBIZ', u'OJB', u'OLINGO', u'OLIO', u'OODT', u'OOZIE', u'ORP', u'OPENEJB', u'OEP', u'OPENJPA', u'OPENMEETINGS', u'OPENNLP', u'OWB', u'ORC', u'PARQUET', u'PDFBOX', u'PHOENIX', u'PHOTARK', u'PIG', u'PIRK', u'PIVOT', u'PLUTO', u'PODLINGNAMESEARCH', u'POLYGENE', u'PORTALS', u'APA', u'PB', u'PIO', u'PROVISIONR', u'PRC', u'HERMES', u'PULSAR', u'PYLUCENE', u'QPID', u'DISPATCH', u'QPIDJMS', u'PROTON', u'RAMPART', u'RAMPARTC', u'RANGER', u'RATIS', u'RAVE', u'REEF', u'RIVER', u'RYA', u'S2GRAPH', u'SAMOA', u'SAMZA', u'SAND', u'SANDESHA2', u'SANDESHA2C', u'SANTUARIO', u'SAVAN', u'SCOUT', u'SENSSOFT', u'SENTRY', u'SERF', u'SM', u'SMX4', u'SMXCOMP', u'SMX4KNL', u'SMX4NMR', u'SHALE', u'SHINDIG', u'SHIRO', u'SINGA', u'SIRONA', u'SLIDER', u'SLING', u'SOAP', u'SOLR', u'SPARK', u'SIS', u'SPOT', u'SQOOP', u'STANBOL', u'STEVE', u'STOMP', u'STONEHENGE', u'STRATOS', u'STREAMS', u'STR', u'WW', u'SB', u'SITE', u'SVN', u'SUPERSET', u'SYNAPSE', u'SYNCOPE', u'SYSTEMML', u'TAJO', u'TAMAYA', u'TAPESTRY', u'TAP5', u'TASHI', u'TEPHRA', u'TST', u'TESTY', u'TEXEN', u'THRIFT', u'TIKA', u'TILES', u'AUTOTAG', u'TEVAL', u'TREQ', u'TILESSB', u'TILESSHARED', u'TILESSHOW', u'TINKERPOP', u'TOMEE', u'TATPI', u'TOREE', u'TORQUE', u'TORQUEOLD', u'TC', u'TS', u'DIRTSEC', u'TRIPLES', u'TSIK', u'TRB', u'TUSCANY', u'UIMA', u'USERGRID', u'VCL', u'VELOCITY', u'VELOCITYSB', u'VELTOOLS', u'VXQUERY', u'VYSPER', u'WADI', u'WAVE', u'WEEX', u'WHIMSY', u'WICKET', u'WINK', u'WODEN', u'WOOKIE', u'WSCOMMONS', u'APOLLO', u'WSRP4J', u'WSS', u'ASFSITE', u'XALANC', u'XALANJ', u'XAP', u'XBEAN', u'XERCESC', u'XERCESP', u'XERCESJ', u'XMLCOMMONS', u'XMLRPC', u'XMLBEANS', u'XGC', u'XMLSCHEMA', u'XW', u'YETUS', u'YOKO', u'ZEPPELIN', u'ZETACOMP', u'ZOOKEEPER']
    for project in all_apache_projects[113:]:
        try:
            jiraIssues("C:\\temp\\apache\\{0}.csv".format(project), "https://issues.apache.org/jira", project)
        except:
            pass


