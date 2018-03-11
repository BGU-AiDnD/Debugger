__author__ = 'amir'

from wekaMethods.articles import *
import networkx
#from wekaMethods.articles import sqlToAttributes
from collections import Counter
import numpy

best_features=[9,10,11,12,15,17,19,20,21,24,26,53,54,55,56,59,61,63,64,65,68,70,75,76,77,78,81,83,85,86,87,90,92,93,94,96,97,103,113,114,115,116,117,118,119,120,130,132,133,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,152,153,72,134,151,155]
class OO:
    def get_attributesOLD(self):
        return [('exception',['true','false']) ,('abstract',['true','false']) ,('serializable',['true','false']) ,
                ( "methods_Count", "NUMERIC"),( "methods_override", "NUMERIC"),( "methods_private_Count", "NUMERIC"),
                ( "methods_avg_params", "NUMERIC"),( "fields_Count", "NUMERIC"),( "fields_private_Count", "NUMERIC"),( "fields_Objects_Count", "NUMERIC"),
                ( "constructors_Count", "NUMERIC"),( "uses_Count", "NUMERIC")]

    def get_featuresOLD(self, c, files_dict,prev_date,start_date,end_date):
        javaDocClassess='select path,exception,abstract,serializable  from classes '
        sqlToAttributes([ "false", "false", "false"], c, files_dict, javaDocClassess)

        countMethds="select classes.path,count(*) from classes,methods where classes.name=methods.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)

        countMethds="select classes.path,cast(count(distinct methods.name) as real)/count(methods.name) from classes,methods where classes.name=methods.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)

        countPrivatesMethds="select classes.path,count(*) from classes,methods where classes.name=methods.className and methods.scope=\"private\" group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countPrivatesMethds)

        avgMethodsParams="select classes.path,avg(methods.Num_params) from classes,methods where classes.name=methods.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, avgMethodsParams)

        countFields="select classes.path,count(*) from classes,fields where classes.name=fields.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countFields)

        countPrivateFields="select classes.path,count(*) from classes,fields where classes.name=fields.className and fields.scope=\"private\" group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countPrivateFields)

        objectFields="select classes.path,count(*) from classes,fields where classes.name=fields.className and fields.type in (select distinct name from classes) group by classes.path"
        sqlToAttributes(["0"], c, files_dict, objectFields)

        countConst="select classes.path,count(*) from classes,constructors where classes.name=constructors.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countConst)

        UsedThis="select classes.path,count(*) from classes,fields where classes.name=fields.type group by classes.path"
        sqlToAttributes(["0"], c, files_dict, UsedThis)


    def classes_features(self,c,files_dict):
        interfaces='select path, superClass from classes where superClass="Interface"'
        sqlToAttributes(["class"], c, files_dict, interfaces)
        interfaces='select path, "No parent" from classes where superClass="java.lang.Object"'
        sqlToAttributes(["Has parent"], c, files_dict, interfaces)
        interfaces='select path ,exception  ,externalizable  ,abstract   ,error  ,case when scope="" then "default" else scope end as b ,serializable from classes'
        sqlToAttributes(["false","false","false","false","public","false"], c, files_dict, interfaces)

    def stat(self,lst):
        counts= Counter(lst)
        return len(lst),sum(lst),numpy.mean(lst),numpy.median(lst),numpy.var(lst),max(lst),min(lst), 1==len(counts)

    def addFromDict(self,files_dict,dict,pathNames):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = [0]
        for d in pathNames:
            if pathNames[d] in Att_dict:
                if d in dict:
                    Att_dict[pathNames[d]]=[round(dict[d],5)]
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]


    def hirarcy(self, c, files_dict):
        edges = []
        interfaces = 'select path, superClass from classes'
        files_Names = [x.split(".")[-1] for x in files_dict]
        pathNames = {}
        for row in c.execute(interfaces):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-1]
            pathNames[nameClass] = row[0]
            nameSuper = (Agent.pathTopack.pathToPack(row[1])).split(".")[-1]
            if (nameClass in files_Names):
                sup = 'root'
                if (nameSuper in files_Names):
                    sup = nameSuper
                edges.append((sup, nameClass))
        g = networkx.DiGraph()
        g.add_edges_from(edges)
        degs = g.out_degree()
        degsIN = g.in_degree()
        succ = dict(networkx.bfs_successors(g, 'root'))
        for s in succ:
            succ[s] = len(succ[s])
        paths = networkx.single_source_dijkstra_path(g, 'root')
        depth = {}
        for n in g.nodes():
            depth[n] = 2
            if (n in paths):
                depth[n] = len(paths[n])
        self.addFromDict(files_dict,degs,pathNames)
        self.addFromDict(files_dict,degsIN,pathNames)
        self.addFromDict(files_dict,succ,pathNames)
        self.addFromDict(files_dict,depth,pathNames)
        return  files_Names,

    def classesGraph(self,c,files_dict,scope):
        edges = []
        interfaces = 'select path, superClass from classes'
        files_Names = [x.split(".")[-1] for x in files_dict]
        pathNames = {}
        for row in c.execute(interfaces):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-1]
            pathNames[nameClass] = row[0]
            nameSuper = (Agent.pathTopack.pathToPack(row[1])).split(".")[-1]
            if (nameClass in files_Names):
                sup = 'root'
                if (nameSuper in files_Names):
                    sup = nameSuper
                edges.append((sup, nameClass))
        g = networkx.DiGraph()
        g.add_edges_from(edges)
        paths = networkx.single_source_dijkstra_path(g, 'root')

        methods={}
        for x in files_Names:
            methods[x]=[]
        methods['root']=[]
        sigsEdges=[]
        interfaces='select classPath,signature,return, name from methods where scope='+scope
        for row in c.execute(interfaces):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-2]
            if nameClass in files_Names:
                methods[nameClass].append(row[3])
            retAdd=[]
            if row[2] in files_Names:
                retAdd=[(nameClass,row[2])]
            sigsEdges.extend([ (nameClass,x) for x in  self.signatureTolst(row[1]) if x in files_Names]+retAdd)

        fields='select classPath, name ,type from fields where scope='+scope
        fields_d={}
        for x in files_Names:
            fields_d[x]=[]
        fields_d['root']=[]
        for row in c.execute(fields):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-2]
            if nameClass in files_Names:
                fields_d[nameClass].append(row[1])
            type_f=[]
            if row[2] in files_Names:
                type_f=[(nameClass,row[2])]
            sigsEdges.extend(type_f)


        g2=networkx.DiGraph()
        g2.add_edges_from(sigsEdges)
        counts= Counter(sigsEdges)

        g3=networkx.DiGraph()
        for e,w in counts.items():
            u,v=e
            g3.add_edge(u,v,weight=w)



        self.addFromDict(files_dict,g2.out_degree(),pathNames)
        self.addFromDict(files_dict,networkx.katz_centrality(g2),pathNames)
        self.addFromDict(files_dict,networkx.core_number(g2),pathNames)
        self.addFromDict(files_dict,networkx.closeness_centrality(g2),pathNames)
        self.addFromDict(files_dict,networkx.degree_centrality(g2),pathNames)
        self.addFromDict(files_dict,networkx.out_degree_centrality(g2),pathNames)
        self.addFromDict(files_dict,g3.out_degree(),pathNames)
        self.addFromDict(files_dict,networkx.core_number(g3),pathNames)
        self.addFromDict(files_dict,networkx.closeness_centrality(g3),pathNames)
        self.addFromDict(files_dict,networkx.degree_centrality(g3),pathNames)
        self.addFromDict(files_dict,networkx.out_degree_centrality(g3),pathNames)
        #gi = igraph.Graph(edges = g2.edges(),directed=True)

        #gi.modularity()

        #self.addFromDict(files_dict,gi.community_optimal_modularity(),pathNames)


        networkx.write_graphml(g,"C:\GitHub\weka\\graph.graphml")


    def signatureTolst(self,signature):
        lst=[]
        for sig in (signature[1:-1]).split(","):
            lst.append(sig)
        return lst

    def methods_features(self,c,files_dict,callingTable,isSimpleMethod):
        countMethds="select classes.path,count(*) from classes,"+callingTable+" where classes.name="+callingTable+".className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)
        primitiveTypes=["'int'","'short'","'long'","'byte'","'float'","'double'", "'char'","'boolean'","'String'"]
        voidType=["'void'"]
        javaLang=["'java.%'"]
        typesSql=[primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
        javaLangPy=["java"]
        typesPy=[primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLangPy]
        for table in ["(select *,1 as total from classes)"]:
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="private" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="protected" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope<>"public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            if isSimpleMethod:
                countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.name like "get%" group by C.path'
                sqlToAttributes(["0"], c, files_dict, countMethds)
                for table in ["(select classes.path as path,classes.name as name,count(*) as total from classes,"+callingTable+" where classes.name="+callingTable+".className group by classes.path)" ]:

                        for t in typesSql:
                            s=(' or '+callingTable+'.name like ').join(t)
                            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and ( '+callingTable+'.return like '+s+') group by C.path'
                            sqlToAttributes(["0"], c, files_dict, countMethds)
                        for t in typesSql:
                            s=(' or '+callingTable+'.name like ').join(t)
                            countMethds='select C.path,count(distinct return)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and ( '+callingTable+'.return like '+s+' ) group by C.path'
                            sqlToAttributes(["0"], c, files_dict, countMethds)
        for table in ["(select *,1 as total from classes)","(select classes.path as path,classes.name as name,count(*) as total from classes,"+callingTable+" where classes.name="+callingTable+".className group by classes.path)" ]:

            signaturesCheck={}
            signaturesTotal={}
            s='select C.path,'+callingTable+'.name,signature,(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className'
            for f in files_dict.keys():
                signaturesCheck[f] = {}
                signaturesTotal[f] = 0
            for row in c.execute(s):
                classname = Agent.pathTopack.pathToPack(row[0])
                if (classname in signaturesCheck):
                    (signaturesCheck[classname])[row[1]] = self.signatureTolst(row[2])
                    signaturesTotal[classname] = int(row[3])
            for t in typesPy:
                out_t={}
                out_t_set={}
                for classname in signaturesCheck:
                    out_t[classname]=[]
                    out_t_set[classname]=[]
                for t1 in t:
                    for classname in signaturesCheck:
                        for n in signaturesCheck[classname]:
                            type_start=[x for x in (signaturesCheck[classname])[n] if x.startswith(t1)]
                            out_t[classname].append(len(type_start)/(1.0*signaturesTotal[classname]))
                            out_t_set[classname].append(len(set(type_start))/(1.0*signaturesTotal[classname]))
                for f in out_t:
                    if out_t[f]==[]:
                        out_t[f]=[0,0,0,0,0,0]
                    files_dict[f] = files_dict[f] + list([len(out_t[f])])
                    if out_t_set[f]==[]:
                        out_t_set[f]=[0,0,0,0,0,0]
                    files_dict[f] = files_dict[f] + list([len(out_t_set[f])])
        params={}
        parQ='select classPath, Num_params  from '+callingTable+''
        for f in files_dict.keys():
            params[f] = [-999]
        for row in c.execute(parQ):
            name = Agent.pathTopack.pathToPack(".".join((row[0].split("."))[:-1]))
            if (name in params):
                (params[name]).append(int(row[1]))
        for f in params:
            if len(params[f])>1:
                params[f].remove(-999)
            files_dict[f] = files_dict[f] + list(self.stat(params[f]))


    def fields_features(self,c,files_dict):
        countMethds="select classes.path,count(*) from classes,fields where classes.name=fields.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)
        primitiveTypes=["'int'","'short'","'long'","'byte'","'float'","'double'", "'char'","'boolean'","'String'"]
        voidType=["'void'"]
        javaLang=["'java.%'"]
        typesSql=[primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
        callingTable='fields'
        for table in ["(select *,1 as total from classes)","(select classes.path as path,classes.name as name,count(*) as total from classes,"+callingTable+" where classes.name="+callingTable+".className group by classes.path)" ]:
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="private" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="protected" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope="public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.scope<>"public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.static="true" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and '+callingTable+'.final="true" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            for t in typesSql:
                    s=(' or '+callingTable+'.name like ').join(t)
                    countMethds='select C.path,count(*)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and ( '+callingTable+'.type like '+s+') group by C.path'
                    sqlToAttributes(["0"], c, files_dict, countMethds)
            for t in typesSql:
                    s=(' or '+callingTable+'.name like ').join(t)
                    countMethds='select C.path,count(distinct type)/(C.total*1.0) from ' +table+' as C,'+callingTable+' where C.name='+callingTable+'.className and ( '+callingTable+'.type like '+s+' ) group by C.path'
                    sqlToAttributes(["0"], c, files_dict, countMethds)

    def get_featuresAll(self, c, files_dict,prev_date,start_date,end_date):
        self.hirarcy(c,files_dict)
        for scope in ['"public"','"protected"','"private"','"public" or scope="protected" or scope="private" or scope=""']:
            self.classesGraph(c,files_dict,scope)
        self.classes_features(c,files_dict)
        self.methods_features(c,files_dict,'methods',True)
        self.methods_features(c,files_dict,'constructors',False)
        self.fields_features(c,files_dict)
        #UsedThis="select classes.path,count(*) from classes,fields where classes.name=fields.type group by classes.path"
        #sqlToAttributes(["0"], c, files_dict, UsedThis)

    def get_attributesAll(self):
        '''('IsInterface',['Interface','class']),('Parent',['Has parent','No parent']) ,
                ('exception',['true','false']) ,('externalizable',['true','false']) ,('abstract',['true','false']) ,('error',['true','false']) ,('scope',['public','protected','private','default'])
            ,('serializable',['true','false']) ,'''
        all= [

("degs", "NUMERIC"),("degsIN", "NUMERIC"),("succ", "NUMERIC"),("depth", "NUMERIC"),
("out_degree_public", "NUMERIC"),("katz_centrality(g2_public", "NUMERIC"),
("core_number(g2_public", "NUMERIC"),("closeness_centrality(g2_public", "NUMERIC"),("degree_centrality(g2_public", "NUMERIC"),("out_degree_centrality(g2_public", "NUMERIC"),
("out_degreeG3_public", "NUMERIC"),("core_number(g3_public", "NUMERIC"),("closeness_centrality(g3_public", "NUMERIC"),("degree_centrality(g3_public", "NUMERIC"),("out_degree_centrality(g3_public", "NUMERIC"),
("out_degree_protected", "NUMERIC"),("katz_centrality(g2_protected", "NUMERIC"),
("core_number(g2_protected", "NUMERIC"),("closeness_centrality(g2_protected", "NUMERIC"),("degree_centrality(g2_protected", "NUMERIC"),("out_degree_centrality(g2_protected", "NUMERIC"),
("out_degreeG3_protected", "NUMERIC"),("core_number(g3_protected", "NUMERIC"),("closeness_centrality(g3_protected", "NUMERIC"),("degree_centrality(g3_protected", "NUMERIC"),("out_degree_centrality(g3_protected", "NUMERIC"),
("out_degree_private", "NUMERIC"),("katz_centrality(g2_private", "NUMERIC"),
("core_number(g2_private", "NUMERIC"),("closeness_centrality(g2_private", "NUMERIC"),("degree_centrality(g2_private", "NUMERIC"),("out_degree_centrality(g2_private", "NUMERIC"),
("out_degreeG3_private", "NUMERIC"),("core_number(g3_private", "NUMERIC"),("closeness_centrality(g3_private", "NUMERIC"),("degree_centrality(g3_private", "NUMERIC"),("out_degree_centrality(g3_private", "NUMERIC"),
("out_degree_all", "NUMERIC"),("katz_centrality(g2_all", "NUMERIC"),
("core_number(g2_all", "NUMERIC"),("closeness_centrality(g2_all", "NUMERIC"),("degree_centrality(g2_all", "NUMERIC"),("out_degree_centrality(g2_all", "NUMERIC"),
("out_degreeG3_all", "NUMERIC"),("core_number(g3_all", "NUMERIC"),("closeness_centrality(g3_all", "NUMERIC"),("degree_centrality(g3_all", "NUMERIC"),("out_degree_centrality(g3_all", "NUMERIC"),
('IsInterface',['Interface','class']),('Parent',['Has parent','No parent']) ,
                ('exception',['true','false']) ,('externalizable',['true','false']) ,('abstract',['true','false']) ,('error',['true','false']) ,('scope',['public','protected','private','default'])
            ,('serializable',['true','false']) ,
                ( "methods_Count", "NUMERIC"),

                ( "methods_private_Count", "NUMERIC"),( "methods_protected_Count", "NUMERIC"),( "methods_public_Count", "NUMERIC"),( "methods_not_public_Count", "NUMERIC"),
                # only Simple
                    ('methods_getters_Count',"NUMERIC"),
                        # for t in typesSql [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        ('methods_return_primitive_Count',"NUMERIC"),('methods_return_void_Count',"NUMERIC"),('methods_return_java_Count',"NUMERIC"),('methods_return_all_Count',"NUMERIC"),
                        ('methods_return_distinct_primitive_Count',"NUMERIC"),('methods_return_distinct_void_Count',"NUMERIC"),('methods_return_distinct_java_Count',"NUMERIC"),('methods_return_distinct_all_Count',"NUMERIC"),
                #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_primitive", "NUMERIC"),
    ( "len_primitive_set", "NUMERIC"),
                        #void
                        ( "len_void", "NUMERIC"),
    ( "len_void_set", "NUMERIC"),
                        #java
                        ( "len_java", "NUMERIC"),
    ( "len_java_set", "NUMERIC"),
                        #all
                        ( "len_all", "NUMERIC"),
    ( "len_all_set", "NUMERIC"),



                # only Simple
                    #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_primitive_percent", "NUMERIC"),
    ( "len_primitive_set_percent", "NUMERIC"),
                        #void
                        ( "len_void_percent", "NUMERIC"),
    ( "len_void_set_percent", "NUMERIC"),
                        #java
                        ( "len_java_percent", "NUMERIC"),
    ( "len_java_set_percent", "NUMERIC"),
                        #all
                        ( "len_all_percent", "NUMERIC"),
    ( "len_all_set_percent", "NUMERIC"),


                ( "len_params", "NUMERIC"),( "sum_params", "NUMERIC"),( "mean_params", "NUMERIC"),( "median_params", "NUMERIC"),
    ( "var_params", "NUMERIC"),( "max_params", "NUMERIC"),( "min_params", "NUMERIC"),( " ONE_elem_params", ['True','False']),
     #constructors

                        ( "constructors_Count", "NUMERIC"),( "constructors_private_Count", "NUMERIC"),( "constructors_protected_Count", "NUMERIC"),( "constructors_public_Count", "NUMERIC"),( "constructors_not_public_Count", "NUMERIC"),
                    #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_constructors__primitive", "NUMERIC"), ( "len_constructors__primitive_set", "NUMERIC"),
                        #void
                        ( "len_constructors__void", "NUMERIC"), ( "len_constructors__void_set", "NUMERIC"),
                        #java
                        ( "len_constructors__java", "NUMERIC"), ( "len_constructors__java_set", "NUMERIC"),
                        #all
                        ( "len_constructors__all", "NUMERIC"), ( "len_constructors__all_set", "NUMERIC"),


                    #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_constructors__primitive_percent", "NUMERIC"), ( "len_constructors__primitive_set_percent", "NUMERIC"),
                        #void
                        ( "len_constructors__void_percent", "NUMERIC"), ( "len_constructors__void_set_percent", "NUMERIC"),
                        #java
                        ( "len_constructors__java_percent", "NUMERIC"), ( "len_constructors__java_set_percent", "NUMERIC"),
                        #all
                        ( "len_constructors__all_percent", "NUMERIC"), ( "len_constructors__all_set_percent", "NUMERIC"),
    ( "len_params_constructors", "NUMERIC"),( "sum_params_constructors", "NUMERIC"),( "mean_params_constructors", "NUMERIC"),( "median_params_constructors", "NUMERIC"),
( "var_params_constructors", "NUMERIC"),( "max_params_constructors", "NUMERIC"),( "min_params_constructors", "NUMERIC"),( " ONE_elem_params_constructors",['True','False']),

                ( "fields_Count", "NUMERIC"),

                ( "fields_private_Count", "NUMERIC"),( "fields_protected_Count", "NUMERIC"),( "fields_public_Count", "NUMERIC"),( "fields_not_public_Count", "NUMERIC"),
                ('fields_static_Count',"NUMERIC"),('fields_final_Count',"NUMERIC"),
                ('fields_type_primitive_Count',"NUMERIC"),('fields_type_void_Count',"NUMERIC"),('fields_type_java_Count',"NUMERIC"),('fields_type_all_Count',"NUMERIC"),
                ('fields_type_distinct_primitive_Count',"NUMERIC"),('fields_type_distinct_void_Count',"NUMERIC"),('fields_type_distinct_java_Count',"NUMERIC"),('fields_type_distinct_all_Count',"NUMERIC"),
                ( "fields_percent_private_Count", "NUMERIC"),( "fields_percent_protected_Count", "NUMERIC"),( "fields_percent_public_Count", "NUMERIC"),( "fields_percent_not_public_Count", "NUMERIC"),
                ('fields_percent_static_Count',"NUMERIC"),('fields_percent_final_Count',"NUMERIC"),
                ('fields_percent_type_primitive_Count',"NUMERIC"),('fields_percent_type_void_Count',"NUMERIC"),('fields_percent_type_java_Count',"NUMERIC"),('fields_percent_type_all_Count',"NUMERIC"),
                ('fields_percent_type_distinct_primitive_Count',"NUMERIC"),('fields_percent_type_distinct_void_Count',"NUMERIC"),('fields_percent_type_distinct_java_Count',"NUMERIC"),('fields_percent_type_distinct_all_Count',"NUMERIC")]


        ret=[]
        for i in range(len(all)):
            if i+1 in best_features or isAll:
                ret.append(all[i])
        return ret


    def get_attributesBest(self):
        '''('IsInterface',['Interface','class']),('Parent',['Has parent','No parent']) ,
                ('exception',['true','false']) ,('externalizable',['true','false']) ,('abstract',['true','false']) ,('error',['true','false']) ,('scope',['public','protected','private','default'])
            ,('serializable',['true','false']) ,'''
        all= [

("degs", "NUMERIC"),("degsIN", "NUMERIC"),("succ", "NUMERIC"),("depth", "NUMERIC"),
("overrideFactor_public", "NUMERIC"),("inheritenceFactor_public", "NUMERIC"),
("inheritenceFactor_fields_public", "NUMERIC"),("in_degree_public", "NUMERIC"),("out_degree_public", "NUMERIC"),("katz_centrality(g2_public", "NUMERIC"),
("core_number(g2_public", "NUMERIC"),("closeness_centrality(g2_public", "NUMERIC"),("betweenness_centrality_source(g2_public", "NUMERIC"),("eigenvector_centrality_g2_public", "NUMERIC"),("degree_centrality(g2_public", "NUMERIC"),("in_degree_centrality(g2_public", "NUMERIC"),("out_degree_centrality(g2_public", "NUMERIC"),
("in_degreeG3_public", "NUMERIC"),("out_degreeG3_public", "NUMERIC"),("core_number(g3_public", "NUMERIC"),("closeness_centrality(g3_public", "NUMERIC"),("betweenness_centrality_source(g3_public", "NUMERIC"),("eigenvector_centrality_g3_public", "NUMERIC"),("degree_centrality(g3_public", "NUMERIC"),("in_degree_centrality(g3_public", "NUMERIC"),("out_degree_centrality(g3_public", "NUMERIC"),
("overrideFactor_protected", "NUMERIC"),("inheritenceFactor_protected", "NUMERIC"),
("inheritenceFactor_fields_protected", "NUMERIC"),("in_degree_protected", "NUMERIC"),("out_degree_protected", "NUMERIC"),("katz_centrality(g2_protected", "NUMERIC"),
("core_number(g2_protected", "NUMERIC"),("closeness_centrality(g2_protected", "NUMERIC"),("betweenness_centrality_source(g2_protected", "NUMERIC"),("eigenvector_centrality_g2_protected", "NUMERIC"),("degree_centrality(g2_protected", "NUMERIC"),("in_degree_centrality(g2_protected", "NUMERIC"),("out_degree_centrality(g2_protected", "NUMERIC"),
("in_degreeG3_protected", "NUMERIC"),("out_degreeG3_protected", "NUMERIC"),("core_number(g3_protected", "NUMERIC"),("closeness_centrality(g3_protected", "NUMERIC"),("betweenness_centrality_source(g3_protected", "NUMERIC"),("eigenvector_centrality_g3_protected", "NUMERIC"),("degree_centrality(g3_protected", "NUMERIC"),("in_degree_centrality(g3_protected", "NUMERIC"),("out_degree_centrality(g3_protected", "NUMERIC"),
("overrideFactor_private", "NUMERIC"),("inheritenceFactor_private", "NUMERIC"),
("inheritenceFactor_fields_private", "NUMERIC"),("in_degree_private", "NUMERIC"),("out_degree_private", "NUMERIC"),("katz_centrality(g2_private", "NUMERIC"),
("core_number(g2_private", "NUMERIC"),("closeness_centrality(g2_private", "NUMERIC"),("betweenness_centrality_source(g2_private", "NUMERIC"),("eigenvector_centrality_g2_private", "NUMERIC"),("degree_centrality(g2_private", "NUMERIC"),("in_degree_centrality(g2_private", "NUMERIC"),("out_degree_centrality(g2_private", "NUMERIC"),
("in_degreeG3_private", "NUMERIC"),("out_degreeG3_private", "NUMERIC"),("core_number(g3_private", "NUMERIC"),("closeness_centrality(g3_private", "NUMERIC"),("betweenness_centrality_source(g3_private", "NUMERIC"),("eigenvector_centrality_g3_private", "NUMERIC"),("degree_centrality(g3_private", "NUMERIC"),("in_degree_centrality(g3_private", "NUMERIC"),("out_degree_centrality(g3_private", "NUMERIC"),
("overrideFactor_all", "NUMERIC"),("inheritenceFactor_all", "NUMERIC"),
("inheritenceFactor_fields_all", "NUMERIC"),("in_degree_all", "NUMERIC"),("out_degree_all", "NUMERIC"),("katz_centrality(g2_all", "NUMERIC"),
("core_number(g2_all", "NUMERIC"),("closeness_centrality(g2_all", "NUMERIC"),("betweenness_centrality_source(g2_all", "NUMERIC"),("eigenvector_centrality_g2_all", "NUMERIC"),("degree_centrality(g2_all", "NUMERIC"),("in_degree_centrality(g2_all", "NUMERIC"),("out_degree_centrality(g2_all", "NUMERIC"),
("in_degreeG3_all", "NUMERIC"),("out_degreeG3_all", "NUMERIC"),("core_number(g3_all", "NUMERIC"),("closeness_centrality(g3_all", "NUMERIC"),("betweenness_centrality_source(g3_all", "NUMERIC"),("eigenvector_centrality_g3_all", "NUMERIC"),("degree_centrality(g3_all", "NUMERIC"),("in_degree_centrality(g3_all", "NUMERIC"),("out_degree_centrality(g3_all", "NUMERIC"),

                ( "methods_Count", "NUMERIC"),

                ( "methods_private_Count", "NUMERIC"),( "methods_protected_Count", "NUMERIC"),( "methods_public_Count", "NUMERIC"),( "methods_not_public_Count", "NUMERIC"),
                ('methods_static_Count',"NUMERIC"),('methods_varArgs_Count',"NUMERIC"),('methods_synchronized_Count',"NUMERIC"),('methods_final_Count',"NUMERIC"),
                # only Simple
                    ('methods_abstract_Count',"NUMERIC"),('methods_getters_Count',"NUMERIC"),('methods_setters_Count',"NUMERIC"),
                        # for t in typesSql [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        ('methods_return_primitive_Count',"NUMERIC"),('methods_return_void_Count',"NUMERIC"),('methods_return_java_Count',"NUMERIC"),('methods_return_all_Count',"NUMERIC"),
                        ('methods_return_distinct_primitive_Count',"NUMERIC"),('methods_return_distinct_void_Count',"NUMERIC"),('methods_return_distinct_java_Count',"NUMERIC"),('methods_return_distinct_all_Count',"NUMERIC"),
                #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_primitive", "NUMERIC"),
    ( "len_primitive_set", "NUMERIC"),
                        #void
                        ( "len_void", "NUMERIC"),
    ( "len_void_set", "NUMERIC"),
                        #java
                        ( "len_java", "NUMERIC"),
    ( "len_java_set", "NUMERIC"),
                        #all
                        ( "len_all", "NUMERIC"),
    ( "len_all_set", "NUMERIC"),



                ( "methods_private_Count_percent", "NUMERIC"),( "methods_protected_Count_percent", "NUMERIC"),( "methods_public_Count_percent", "NUMERIC"),( "methods_not_public_Count_percent", "NUMERIC"),
                ('methods_static_Count_percent',"NUMERIC"),('methods_varArgs_Count_percent',"NUMERIC"),('methods_synchronized_Count_percent',"NUMERIC"),('methods_final_Count_percent',"NUMERIC"),
                # only Simple
                    ('methods_abstract_Count_percent',"NUMERIC"),('methods_getters_Count_percent',"NUMERIC"),('methods_setters_Count_percent',"NUMERIC"),
                        # for t in typesSql [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        ('methods_return_primitive_Count_percent',"NUMERIC"),('methods_return_void_Count_percent',"NUMERIC"),('methods_return_java_Count_percent',"NUMERIC"),('methods_return_all_Count_percent',"NUMERIC"),
                        ('methods_return_distinct_primitive_Count_percent',"NUMERIC"),('methods_return_distinct_void_Count_percent',"NUMERIC"),('methods_return_distinct_java_Count_percent',"NUMERIC"),('methods_return_distinct_all_Count_percent',"NUMERIC"),
                    #signature [primitiveTypes,voidType,javaLang,primitiveTypes+voidType+javaLang]
                        #primitive
                        ( "len_primitive_percent", "NUMERIC"),
    ( "len_primitive_set_percent", "NUMERIC"),
                        #void
                        ( "len_void_percent", "NUMERIC"),
    ( "len_void_set_percent", "NUMERIC"),
                        #java
                        ( "len_java_percent", "NUMERIC"),
    ( "len_java_set_percent", "NUMERIC"),
                        #all
                        ( "len_all_percent", "NUMERIC"),
    ( "len_all_set_percent", "NUMERIC"),


                ( "len_params", "NUMERIC"),( "sum_params", "NUMERIC"),( "mean_params", "NUMERIC"),( "median_params", "NUMERIC"),
    ( "var_params", "NUMERIC"),( "max_params", "NUMERIC"),( "min_params", "NUMERIC"),( " ONE_elem_params", ['True','False'])]

        ret=[]
        for i in range(len(all)):
            if i+1 in best_features:
                ret.append(all[i])
        return ret


    def get_featuresBest(self, c, files_dict,prev_date,start_date,end_date):
        #self.hirarcy(c,files_dict)
        for scope in ['"public"','"private"','"public" or scope="protected" or scope="private" or scope=""']:
            self.classesGraph(c,files_dict,scope)
        #self.classes_features(c,files_dict)
        self.methods_features(c,files_dict,'methods',True)
        #self.methods_features(c,files_dict,'constructors',False)
        #self.fields_features(c,files_dict)


    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        self.get_featuresBest( c, files_dict,prev_date,start_date,end_date)


    def get_attributes(self):
        return self.get_attributesBest()