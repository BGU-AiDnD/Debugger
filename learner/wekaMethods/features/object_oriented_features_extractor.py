import json
from os import path
from collections import Counter

import numpy
import networkx

from wekaMethods.articles import *
from wekaMethods.features.features_extractor import FeaturesExtractor


# TODO: Amir add documentation please :)
class ObjectOrientedFeaturesExtractor(FeaturesExtractor):
    """"""

    VOID_TYPE = ["'void'"]
    JAVA_LANG_ANNOTATION = ["'java.%'"]
    PRIMITIVE_TYPES = ["'int'", "'short'", "'long'", "'byte'", "'float'", "'double'", "'char'",
                       "'boolean'", "'String'"]

    BASIC_GENERIC_TYPES = VOID_TYPE + PRIMITIVE_TYPES

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

    def extract_statistical_features(self, lst):
        """"""
        counts = Counter(lst)
        return len(lst), sum(lst), numpy.mean(lst), numpy.median(lst), numpy.var(lst), max(lst), \
               min(lst), 1 == len(counts)

    # TODO: check this method
    def add_attributes(self, attributes_dict, path_names):
        """"""
        attributes = {file_name: [0] for file_name in self.files_map}

        for path_name, path_data in path_names.items():
            if path_data in attributes and path_name in attributes_dict:
                attributes[path_names[path_name]] = [round(attributes_dict[path_name], 5)]

        for file_name in attributes:
            self.files_map[file_name] += attributes[file_name]

    def create_classes_graph(self, scope):
        files_names = [x.split(".")[-1] for x in self.files_map]
        path_names = {}

        directed_graph = self.extract_super_classes_graph_data(files_names, path_names)
        signature_edges = self.extract_signatures_edges(files_names, scope)
        self.extract_fields_edges_data(files_names, scope, signature_edges)

        signatures_directed_graph = networkx.DiGraph()
        signatures_directed_graph.add_edges_from(signature_edges)
        counts = Counter(signature_edges)

        weighted_graph = networkx.DiGraph()
        for edge_vertexes, weight in counts.items():
            u, v = edge_vertexes
            weighted_graph.add_edge(u, v, weight=weight)

        self.add_attributes(signatures_directed_graph.out_degree(), path_names)
        self.add_attributes(networkx.katz_centrality(signatures_directed_graph), path_names)
        self.add_attributes(networkx.core_number(signatures_directed_graph), path_names)
        self.add_attributes(networkx.closeness_centrality(signatures_directed_graph), path_names)
        self.add_attributes(networkx.degree_centrality(signatures_directed_graph), path_names)
        self.add_attributes(networkx.out_degree_centrality(signatures_directed_graph), path_names)
        self.add_attributes(weighted_graph.out_degree(), path_names)
        self.add_attributes(networkx.core_number(weighted_graph), path_names)
        self.add_attributes(networkx.closeness_centrality(weighted_graph), path_names)
        self.add_attributes(networkx.degree_centrality(weighted_graph), path_names)
        self.add_attributes(networkx.out_degree_centrality(weighted_graph), path_names)

        # TODO: change to a folder that is available in linux as well
        networkx.write_graphml(directed_graph, "C:\GitHub\weka\\graph.graphml")

    def extract_fields_edges_data(self, files_names, scope, signature_edges):
        """"""
        class_fields_data_query = 'select classPath, name, type from fields ' \
                                  'where scope={scope}'.format(scope=scope)
        class_fields = {file_name: [] for file_name in files_names}
        class_fields['root'] = []
        for class_path, field_name, field_type in \
                self.cursor_object.execute(class_fields_data_query):
            class_name = Agent.pathTopack.pathToPack(class_path).split(".")[-2]
            if class_name in files_names:
                class_fields[class_name].append(field_name)

            class_field_types = [(class_name, field_type)] if field_type in files_names else []
            signature_edges.extend(class_field_types)

    def extract_signatures_edges(self, files_names, scope):
        """"""
        methods = {file_name: [] for file_name in files_names}
        methods['root'] = []
        signature_edges = []
        classes_signatures_query = 'select classPath, signature, return, name ' \
                                   'from methods where scope={scope}'.format(scope=scope)
        for class_path, signature, return_addr, method_name in \
                self.cursor_object.execute(classes_signatures_query):
            class_name = (Agent.pathTopack.pathToPack(class_path)).split(".")[-2]
            if class_name in files_names:
                methods[class_name].append(method_name)

            class_return_addrres = [(class_name, return_addr)] if return_addr in files_names else []

            relevant_class_method_signatures = [(class_name, signature) for signature in
                                                self.split_signatures(signature)
                                                if signature in files_names]
            signature_edges.extend(relevant_class_method_signatures + class_return_addrres)
        return signature_edges

    def extract_super_classes_graph_data(self, files_names, path_names):
        """"""
        edges = []
        super_classes_paths_query = 'select path, superClass from classes'

        for path_name, super_class in self.cursor_object.execute(super_classes_paths_query):
            class_name = (Agent.pathTopack.pathToPack(path_name)).split(".")[-1]
            path_names[class_name] = path_name
            super_class_name = (Agent.pathTopack.pathToPack(super_class)).split(".")[-1]

            if class_name in files_names:
                sup = 'root'
                if super_class_name in files_names:
                    sup = super_class_name

                edges.append((sup, class_name))
        directed_graph = networkx.DiGraph()
        directed_graph.add_edges_from(edges)
        return directed_graph

    def split_signatures(self, signatures_line):
        """Extract the signatures from the extracted signature line.

        Args:
            signatures_line (str): the line extracted from the SQL query.

        Returns:
            list. The signatures that were contained in the line.
        """
        return signatures_line[1:-1].split(",")

    def methods_features(self, cursor, files_dict, calling_table, is_simple_method):
        """"""
        class_methods_count_query = \
            "select classes.path, count(*) from classes," + calling_table + \
            " where classes.name=" + calling_table + ".className group by classes.path"
        self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

        sql_data_types = [self.PRIMITIVE_TYPES, self.VOID_TYPE, self.JAVA_LANG_ANNOTATION,
                          self.BASIC_GENERIC_TYPES + self.JAVA_LANG_ANNOTATION]

        python_data_types = [self.PRIMITIVE_TYPES, self.VOID_TYPE, self.JAVA_LANG_ANNOTATION,
                             self.BASIC_GENERIC_TYPES + ["java"]]

        #TODO: Fix queries names.
        for table in ["(select *,1 as total from classes)"]:
            class_methods_count_query = \
                'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + calling_table + \
                ' where C.name=' + calling_table + '.className and ' + calling_table + \
                '.scope="private" group by C.path'
            self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

            class_methods_count_query = \
                'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + calling_table + \
                ' where C.name=' + calling_table + '.className and ' + calling_table + \
                '.scope="protected" group by C.path'
            self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

            class_methods_count_query = \
                'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + calling_table + \
                ' where C.name=' + calling_table + '.className and ' + calling_table + \
                '.scope="public" group by C.path'
            self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

            class_methods_count_query = \
                'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + calling_table \
                + ' where C.name=' + calling_table + '.className and ' + calling_table \
                + '.scope<>"public" group by C.path'
            self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

            if is_simple_method:
                class_methods_count_query = \
                    'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' \
                    + calling_table + ' where C.name=' + calling_table + '.className and ' \
                    + calling_table + '.name like "get%" group by C.path'
                self.convert_sql_queries_to_attributes(["0"], class_methods_count_query)

                for table in [
                    "(select classes.path as path, classes.name as name, "
                    "count(*) as total from classes," + calling_table +
                    " where classes.name=" + calling_table + ".className group by classes.path)"]:

                    for t in sql_data_types:
                        s = (' or ' + calling_table + '.name like ').join(t)
                        class_methods_count_query = 'select C.path,count(*)/(C.total*1.0) from ' + table + ' as C,' + calling_table + ' where C.name=' + calling_table + '.className and ( ' + calling_table + '.return like ' + s + ') group by C.path'
                        sqlToAttributes(["0"], cursor, files_dict, class_methods_count_query)
                    for t in sql_data_types:
                        s = (' or ' + calling_table + '.name like ').join(t)
                        class_methods_count_query = 'select C.path,count(distinct return)/(C.total*1.0) from ' + table + ' as C,' + calling_table + ' where C.name=' + calling_table + '.className and ( ' + calling_table + '.return like ' + s + ' ) group by C.path'
                        sqlToAttributes(["0"], cursor, files_dict, class_methods_count_query)

        for table in ["(select *,1 as total from classes)",
                      "(select classes.path as path,classes.name as name,count(*) as total from classes," + calling_table + " where classes.name=" + calling_table + ".className group by classes.path)"]:

            signaturesCheck = {}
            signaturesTotal = {}
            s = 'select C.path,' + calling_table + '.name,signature,(C.total*1.0) from ' + table + ' as C,' + calling_table + ' where C.name=' + calling_table + '.className'
            for f in files_dict.keys():
                signaturesCheck[f] = {}
                signaturesTotal[f] = 0
            for row in cursor.execute(s):
                classname = Agent.pathTopack.pathToPack(row[0])
                if (classname in signaturesCheck):
                    (signaturesCheck[classname])[row[1]] = self.split_signatures(row[2])
                    signaturesTotal[classname] = int(row[3])
            for t in python_data_types:
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
        parQ = 'select classPath, Num_params  from ' + calling_table + ''
        for f in files_dict.keys():
            params[f] = [-999]
        for row in cursor.execute(parQ):
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
        for scope in ['"public"', '"private"',
                      '"public" or scope="protected" or scope="private" or scope=""']:
            self.create_classes_graph(scope)
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
