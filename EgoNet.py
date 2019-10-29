import Circle

class EgoNet:
    def __init__(self,ego,ego_net_features):
        self.__ego = ego #Represents the Ego node for the EgoNet. type - Node object
        self.__social_network = {} # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__social_network[ego] = set() # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__alter_node_count = 0 # Represents the total number of alter nodes connected to our Ego
        self.__circles = {} #Represents the circles formed in our EgoNet. type - dict where key = circle name		      and value = set of Node objects in the circle
        self.__ego_net_features = ego_net_features # Represents the features for our Ego Net. type - dict where key = feature			           position in feature file (type - int) and value = tuple of feature name and			          feature id. This does not contain Feature objects but just strings. 


    def get_alter_node(self,node_id):
        for key in self.__social_network:
            if key.get_id() == node_id:
                return key
        return None
        '''
        Function takes a node id
        returns the node object if found by id, else return none
        '''
        
    def get_ego(self):
        return self.__ego
        '''
        returns the ego object
        '''
    
    def get_circle_names(self):
        l = list()
        for key in self.__circles:
            l.append(key)
        return l
        '''
        gets all the names of circles in a list
        returns list
        '''

    def get_circle(self, circle_name):
        return self.__circles[circle_name]
        '''
        get a circle object by its name
        return specified circle
        '''
    
    def get_alters(self):
        return set(self.__social_network[self.__ego])
        '''
        get a set of all alters
        return set
        '''

    def get_alter_node_count(self):
        return int(self.__alter_node_count)
        '''
        get total amount of alter nodes
        return total alter nodes as int
        '''

    def get_ego_net_features(self):
        return self.__ego_net_features
        '''
        gets the features within the ego net
        returns features (dict)
        '''

    def get_ego_net_feature(self, feature):
        return self.__ego_net_features[feature]
        '''
        get a specific ego net feature by name as parameter
        return specific feature
        '''

    def get_feature_pos(self, feature_name, feature_id):
        for key, value in self.__ego_net_features.items():
            if str(value[0]) == feature_name and int(value[1]) == feature_id:
                return key
        return None
        '''
        gets the position of a feature given its name and ID
        returns the feature position, if not found returns none
        '''
    
    def get_alter_connections(self, alter):
        return self.__social_network[alter]
        '''
        get the connections of all the alters and return the dict
        '''
    
    def add_circle(self, circle_name, alters):
        self.__circles[circle_name] = Circle.Circle(circle_name, alters)
        
        '''
        add a circle given circle_name and alters list
        adds to circle dict
        '''
    
    def add_connection_between_alters(self,alter1,alter2):
        self.__social_network[alter1].add(alter2)
        self.__social_network[alter2].add(alter1)
    
        '''
        adds a connection between alters
        takes two alters as arguments, and adds to their connections
        '''

    def add_alter_node(self, alter):
        self.__alter_node_count += 1
        self.__social_network[self.__ego].add(alter)
        if alter not in self.__social_network.keys():
            self.__social_network[alter] = set()
            self.__social_network[alter].add(self.__ego)
        else:
            self.__social_network[alter].add(self.__ego)
            
            '''
            takes an alter node obejct as input
            adds node to the network
            '''

    def __eq__(self,other):
        '''True if all attributes are equal.'''
        return (self.__ego == other.__ego)\
            and (self.__social_network == other.__social_network) \
            and (self.__alter_node_count == other.__alter_node_count) \
            and (self.__circles == other.__circles) \
            and (self.__ego_net_features == other.__ego_net_features)
            
    def __str__(self):
        '''Returns a string representation for printing.'''
        st = f"Ego: {self.__ego}\n"
        st+= f"Social Network: {self.__social_network}\n"
        st+= f"Circles: {self.__circles}"
        return st

    __repr__ = __str__
    