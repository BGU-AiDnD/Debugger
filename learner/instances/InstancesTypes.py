
TYPES = ['class', 'method', 'line']

class Instance(object):
    def __init__(self, instance_type, id, commit, bug):
        assert instance_type in TYPES
        self.instance_type = instance_type
        self.id = id
        self.commit = commit
        self.bug = bug