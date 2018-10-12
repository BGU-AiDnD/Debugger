import json
from os import path

import numpy
import networkx
from collections import Counter

from wekaMethods.articles import *
from wekaMethods.features.features_extractor import FeaturesExtractor

class ObjectOrientedFeaturesExtractor(FeaturesExtractor):
    """"""

    @cached_property
    def features_object(self):
        with open(path.abspath(path.join(self.FEATURES_FOLDER, "object_oriented_features.json")),
                  "r") as features_file:
            return json.load(features_file)

    def get_features(self, prev_date, start_date, end_date):
        pass

    def classes_features(self):
        interfaces_path_and_superclass_query = \
            'select path, superClass from classes where superClass="Interface"'
        self.convert_sql_queries_to_attributes(["class"], interfaces_path_and_superclass_query)

        classes_path_and_parents_query = \
            'select path, "No parent" from classes where superClass="java.lang.Object"'
        self.convert_sql_queries_to_attributes(["Has parent"], classes_path_and_parents_query)

        classes_metadata_query = \
            'select path, exception, externalizable, abstract, error, ' \
            'case when scope="" then "default" else scope end as b, serializable from classes'
        self.convert_sql_queries_to_attributes(
            ["false", "false", "false", "false", "public", "false"], classes_metadata_query)

    def extract_statistical_features(self, lst):    # TODO: What do you use this method for??
        counts = Counter(lst)
        return len(lst), sum(lst), numpy.mean(lst), numpy.median(lst), numpy.var(lst), max(
            lst), min(lst), 1 == len(counts)

    def addFromDict(self, dict, pathNames):
        attributes = {file_name: [0] for file_name in self.files_map}
        for path_name, path_data in pathNames.items():
            if path_data in attributes and path_name in dict:
                attributes[pathNames[path_name]] = [round(dict[path_name], 5)]

        for file_name in attributes:
            self.files_map[file_name] += attributes[file_name]

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
        self.addFromDict(files_dict, degs, pathNames)
        self.addFromDict(files_dict, degsIN, pathNames)
        self.addFromDict(files_dict, succ, pathNames)
        self.addFromDict(files_dict, depth, pathNames)
        return files_Names,

    def classes_graph(self, c, files_dict, scope):
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

        methods = {}
        for x in files_Names:
            methods[x] = []
        methods['root'] = []
        sigsEdges = []
        interfaces = 'select classPath,signature,return, name from methods where scope=' + scope
        for row in c.execute(interfaces):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-2]
            if nameClass in files_Names:
                methods[nameClass].append(row[3])
            retAdd = []
            if row[2] in files_Names:
                retAdd = [(nameClass, row[2])]
            sigsEdges.extend(
                [(nameClass, x) for x in self.signatureTolst(row[1]) if x in files_Names] + retAdd)

        fields = 'select classPath, name ,type from fields where scope=' + scope
        fields_d = {}
        for x in files_Names:
            fields_d[x] = []
        fields_d['root'] = []
        for row in c.execute(fields):
            nameClass = (Agent.pathTopack.pathToPack(row[0])).split(".")[-2]
            if nameClass in files_Names:
                fields_d[nameClass].append(row[1])
            type_f = []
            if row[2] in files_Names:
                type_f = [(nameClass, row[2])]
            sigsEdges.extend(type_f)

        g2 = networkx.DiGraph()
        g2.add_edges_from(sigsEdges)
        counts = Counter(sigsEdges)

        g3 = networkx.DiGraph()
        for e, w in counts.items():
            u, v = e
            g3.add_edge(u, v, weight=w)

        self.addFromDict(files_dict, g2.out_degree(), pathNames)
        self.addFromDict(files_dict, networkx.katz_centrality(g2), pathNames)
        self.addFromDict(files_dict, networkx.core_number(g2), pathNames)
        self.addFromDict(files_dict, networkx.closeness_centrality(g2), pathNames)
        self.addFromDict(files_dict, networkx.degree_centrality(g2), pathNames)
        self.addFromDict(files_dict, networkx.out_degree_centrality(g2), pathNames)
        self.addFromDict(files_dict, g3.out_degree(), pathNames)
        self.addFromDict(files_dict, networkx.core_number(g3), pathNames)
        self.addFromDict(files_dict, networkx.closeness_centrality(g3), pathNames)
        self.addFromDict(files_dict, networkx.degree_centrality(g3), pathNames)
        self.addFromDict(files_dict, networkx.out_degree_centrality(g3), pathNames)
        # gi = igraph.Graph(edges = g2.edges(),directed=True)

        # gi.modularity()

        # self.addFromDict(files_dict,gi.community_optimal_modularity(),pathNames)

        networkx.write_graphml(g, "C:\GitHub\weka\\graph.graphml")

    def signatureTolst(self, signature):
        lst = []
        for sig in (signature[1:-1]).split(","):
            lst.append(sig)
        return lst

    def methods_features(self, c, files_dict, callingTable, isSimpleMethod):
        countMethds = "select classes.path,count(*) from classes," + callingTable + " where classes.name=" + callingTable + ".className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)
        primitiveTypes = ["'int'", "'short'", "'long'", "'byte'", "'float'", "'double'", "'char'",
                          "'boolean'", "'String'"]
        voidType = ["'void'"]
        javaLang = ["'java.%'"]
        typesSql = [primitiveTypes, voidType, javaLang, primitiveTypes + voidType + javaLang]
        javaLangPy = ["java"]
        typesPy = [primitiveTypes, voidType, javaLang, primitiveTypes + voidType + javaLangPy]
        for table in ["(select *,1 as total from classes)"]:
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="private" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="protected" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope<>"public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            if isSimpleMethod:
                countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.name like "get%" group by C.path'
                sqlToAttributes(["0"], c, files_dict, countMethds)
                for table in [
                    "(select classes.path as path,classes.name as name,count(*) as total from classes," + callingTable + " where classes.name=" + callingTable + ".className group by classes.path)"]:

                    for t in typesSql:
                        s = (' or ' + callingTable + '.name like ').join(t)
                        countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ( ' + callingTable + '.return like ' + s + ') group by C.path'
                        sqlToAttributes(["0"], c, files_dict, countMethds)
                    for t in typesSql:
                        s = (' or ' + callingTable + '.name like ').join(t)
                        countMethds = 'select C.path,count(distinct return)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ( ' + callingTable + '.return like ' + s + ' ) group by C.path'
                        sqlToAttributes(["0"], c, files_dict, countMethds)
        for table in ["(select *,1 as total from classes)",
                      "(select classes.path as path,classes.name as name,count(*) as total from classes," + callingTable + " where classes.name=" + callingTable + ".className group by classes.path)"]:

            signaturesCheck = {}
            signaturesTotal = {}
            s = 'select C.path,' + callingTable + '.name,signature,(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className'
            for f in files_dict.keys():
                signaturesCheck[f] = {}
                signaturesTotal[f] = 0
            for row in c.execute(s):
                classname = Agent.pathTopack.pathToPack(row[0])
                if (classname in signaturesCheck):
                    (signaturesCheck[classname])[row[1]] = self.signatureTolst(row[2])
                    signaturesTotal[classname] = int(row[3])
            for t in typesPy:
                out_t = {}
                out_t_set = {}
                for classname in signaturesCheck:
                    out_t[classname] = []
                    out_t_set[classname] = []
                for t1 in t:
                    for classname in signaturesCheck:
                        for n in signaturesCheck[classname]:
                            type_start = [x for x in (signaturesCheck[classname])[n] if
                                          x.startswith(t1)]
                            out_t[classname].append(
                                len(type_start) / (1.0 * signaturesTotal[classname]))
                            out_t_set[classname].append(
                                len(set(type_start)) / (1.0 * signaturesTotal[classname]))
                for f in out_t:
                    if out_t[f] == []:
                        out_t[f] = [0, 0, 0, 0, 0, 0]
                    files_dict[f] = files_dict[f] + list([len(out_t[f])])
                    if out_t_set[f] == []:
                        out_t_set[f] = [0, 0, 0, 0, 0, 0]
                    files_dict[f] = files_dict[f] + list([len(out_t_set[f])])
        params = {}
        parQ = 'select classPath, Num_params  from ' + callingTable + ''
        for f in files_dict.keys():
            params[f] = [-999]
        for row in c.execute(parQ):
            name = Agent.pathTopack.pathToPack(".".join((row[0].split("."))[:-1]))
            if (name in params):
                (params[name]).append(int(row[1]))
        for f in params:
            if len(params[f]) > 1:
                params[f].remove(-999)
            files_dict[f] = files_dict[f] + list(self.extract_statistical_features(params[f]))

    def fields_features(self, c, files_dict):
        countMethds = "select classes.path,count(*) from classes,fields where classes.name=fields.className group by classes.path"
        sqlToAttributes(["0"], c, files_dict, countMethds)
        primitiveTypes = ["'int'", "'short'", "'long'", "'byte'", "'float'", "'double'", "'char'",
                          "'boolean'", "'String'"]
        voidType = ["'void'"]
        javaLang = ["'java.%'"]
        typesSql = [primitiveTypes, voidType, javaLang, primitiveTypes + voidType + javaLang]
        callingTable = 'fields'
        for table in ["(select *,1 as total from classes)",
                      "(select classes.path as path,classes.name as name,count(*) as total from classes," + callingTable + " where classes.name=" + callingTable + ".className group by classes.path)"]:
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="private" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="protected" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope="public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.scope<>"public" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.static="true" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ' + callingTable + '.final="true" group by C.path'
            sqlToAttributes(["0"], c, files_dict, countMethds)
            for t in typesSql:
                s = (' or ' + callingTable + '.name like ').join(t)
                countMethds = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ( ' + callingTable + '.type like ' + s + ') group by C.path'
                sqlToAttributes(["0"], c, files_dict, countMethds)
            for t in typesSql:
                s = (' or ' + callingTable + '.name like ').join(t)
                countMethds = 'select C.path,count(distinct type)/(C.total*1.0) from ' + table + ' as C,' + callingTable + ' where C.name=' + callingTable + '.className and ( ' + callingTable + '.type like ' + s + ' ) group by C.path'
                sqlToAttributes(["0"], c, files_dict, countMethds)

    def get_featuresBest(self, c, files_dict, prev_date, start_date, end_date):
        # self.hirarcy(c,files_dict)
        for scope in ['"public"', '"private"',
                      '"public" or scope="protected" or scope="private" or scope=""']:
            self.classes_graph(c, files_dict, scope)
        self.methods_features(c, files_dict, 'methods', True)

    def get_features(self, c, files_dict, prev_date, start_date, end_date):
        self.get_featuresBest(c, files_dict, prev_date, start_date, end_date)

    def get_attributes(self):
        best_attributes = [attribute_item for index, attribute_item in
                enumerate(self.all_features) if index in self.best_features_indexes]

        result = []
        for attribute in best_attributes:
            attribute_tuples = [(key, attribute[key]) for key in attribute]
            result += attribute_tuples

        return result
