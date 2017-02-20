__author__ = 'amir'

import Ochiai_Rank

class St_Strip:
    def __init__(self,M,N):
        """
        :param M: components No.
        :param N: sets No.
        """
        self.comps={}
        for x in range(M):
            self.comps[x]=False
        self.conflicts={}
        for x in range(N):
            self.conflicts[x]=False

        self.last_unstripped_comps=[]
        self.last_unstripped_confs=[]

        self.conflict_list=[]
        self.unstripped_confs_array=[]
        self.unstripped_comps_array=[]

        self.ochiai_ranks={}

    def setup(self,comps,conflicts,last_unstripped_comps,last_unstripped_confs):
        self.comps=dict(comps)
        self.conflicts=dict(conflicts)

        self.last_unstripped_comps=last_unstripped_comps
        self.last_unstripped_confs=last_unstripped_confs

        self.conflict_list=[]
        self.last_unstripped_confs=[]
        self.unstripped_confs_array=[]
        self.unstripped_comps_array=[]


        self.ochiai_ranks={}

    def get_conflic_list(self,errors):
        if self.conflict_list!=[]:
            return self.conflict_list
        else:
            self.conflict_list=[]
            for index,e in enumerate(errors):
                if e==1 and index in self.conflicts and self.conflicts[index]==False:
                    self.conflict_list.append(index)
        return self.conflict_list

    def clone_ochiai_ranks(self):
        clone= {}
        for i in self.ochiai_ranks:
            clone[i]=self.ochiai_ranks[i].clone()
        return clone

    def clone(self):
        cloneStrip=St_Strip(0,0)
        cloneStrip.setup(self.comps,self.conflicts,self.last_unstripped_comps,self.last_unstripped_confs)
        cloneStrip.ochiai_ranks=self.clone_ochiai_ranks()
        return cloneStrip

    def strip_comp(self,comp):
        self.comps[comp]=True
        self.last_unstripped_comps = self.unstripped_comps_array
        self.unstripped_comps_array=[]


    def strip_conf(self,conf):
        self.conflicts[conf]=True
        self.last_unstripped_confs = self.unstripped_confs_array
        self.unstripped_confs_array=[]

    def is_comp_stripped(self,comp):
        return self.comps[comp]


    def is_conf_stripped(self,conflict):
        return self.conflicts[conflict]

    def update_ochiai_ranks(self,M_matrix, e_vector,  removed_confs, removed_comp):
        conf=-1

#		#if ranks are initial, no need to update

        if (len(self.ochiai_ranks) == 0):
            return
#		#make sure unstripped arrays are not null
        self.unstripped_comps_array_Func()
        self.unstripped_confs_array_Func()

        if removed_confs!=[]:
            for conf in removed_confs:
                for comp in self.unstripped_comps_array:
                    if removed_comp==comp:
                        continue
                    if (M_matrix[conf][comp] == 1 and e_vector[conf] == 1):
                        self.ochiai_ranks[comp].reduce_counter(1, 1)
                    elif (M_matrix[conf][comp] == 0 and e_vector[conf] == 1):
                        self.ochiai_ranks[comp].reduce_counter(0, 1)
                    elif (M_matrix[conf][comp] == 1 and e_vector[conf] == 0):
                        self.ochiai_ranks[comp].reduce_counter(1, 0)

        comp = removed_comp
        for conflict in self.unstripped_confs_array:
            if (M_matrix[conflict][comp] == 1 and e_vector[conflict] == 1):
                self.ochiai_ranks[comp].reduce_counter(1, 1)
			
            elif (M_matrix[conflict][comp] == 0 and e_vector[conflict] == 1):
                self.ochiai_ranks[comp].reduce_counter(0, 1)
			
            elif (M_matrix[conflict][comp] == 1 and e_vector[conflict] == 0):
                self.ochiai_ranks[comp].reduce_counter(1, 0)

    def calc_ochiai_ranks(self, M_matrix, e_vector):
        result = {}
        for i in range(len(M_matrix[0])):
            self.ochiai_ranks[i] = Ochiai_Rank.Ochiai_Rank()
        unstripped_confs = self.unstripped_confs_array_Func()
        unstripped_comps = self.unstripped_comps_array_Func()
        for conf in unstripped_confs:
            for comp in unstripped_comps:
                self.ochiai_ranks[comp].advance_counter(M_matrix[conf][comp], e_vector[conf])
        for i in range(len(M_matrix[0])):
            result[i] = self.ochiai_ranks[i].get_rank()
        return result

    def strip(self, M_matrix,  e_vector,  comp):
        unstripped_confs = self.unstripped_confs_array_Func()
        removed_confs = []

        self.unstripped_comps_array_Func()
        self.unstripped_confs_array_Func()

        for  conf in unstripped_confs:
            if (M_matrix[conf][comp] == 1 and e_vector[conf] == 1):
                self.strip_conf(conf)
                removed_confs.append(conf)

        self.strip_comp(comp)
		
        # removed_confs_array = list(removed_confs)
        # self.update_ochiai_ranks(M_matrix, e_vector, removed_confs_array, comp)

        self.last_unstripped_comps = self.unstripped_comps_array
        self.last_unstripped_confs = self.unstripped_confs_array
        self.unstripped_comps_array = []
        self.unstripped_confs_array = []
        
        
    def unstripped_comps_array_Func(self):
        list = []
        if (self.unstripped_comps_array == [] and self.last_unstripped_comps != []):
            for comp in self.last_unstripped_comps:
                if (self.comps[comp] != True):
                    list.append(comp)

            self.unstripped_comps_array = list
            self.last_unstripped_comps = self.unstripped_comps_array #seems wrong but it's right!

        elif (self.unstripped_comps_array == []):

            for i in range(len(self.comps)):
                if (self.comps[i] != True):
                    list.append(i)

            self.unstripped_comps_array = list

        return self.unstripped_comps_array

    def unstripped_confs_array_Func(self):
        list=[]
        if (self.unstripped_confs_array == [] and self.last_unstripped_confs != []):
            for conf in self.last_unstripped_confs:
                if (not self.conflicts[conf]):
                    list.append(conf)
            self.last_unstripped_confs = self.unstripped_confs_array
            self.unstripped_confs_array = list

        elif (self.unstripped_confs_array == []):
            for i in range(len(self.conflicts)):
                if (self.conflicts[i] != True):
                    list.append(i)
            self.unstripped_confs_array = list
        return self.unstripped_confs_array
