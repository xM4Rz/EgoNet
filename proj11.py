'''
CSE 231 Project 11
User is prompted to enter a user id to generate the ego net
User is then prompted for what he wants to calculate from the ego net
Choices for Ego Net calculation:
    1 - Top 5 similar features in a circle"
    2 - Calculate effective size of Ego Net"
    3 - Calculate circle E/I index"
    4 - Calculate Ego Net efficiency
    q/Q - Quit
The user chooses an option, then  is prompted to to give more info
    to complete the calculation
The user is shown the calculation, then is reprompted to choose a calculation

'''





from EgoNet import EgoNet
from Node import Node
from Feature import Feature
from Circle import Circle
from operator import itemgetter

def get_ego_net_files():
    y1 = "_ego_features.txt"
    y2 = "_ego_net_features.txt"
    y3 = "_alters_features.txt"
    y4 = "_ego_net_connections.txt"
    y5 = "_circles.txt"
    x = input("Enter user id to generate EgoNet: ")
    while True:
        try:
            fp1 = open(x+y1)
            fp2 = open(x+y2)
            fp3 = open(x+y3)
            fp4 = open(x+y4)
            fp5 = open(x+y5)

            return (int(x),fp1,fp2,fp3,fp4,fp5)

        except FileNotFoundError:
            print("File not found for ego_id: ",x)
            x = input("Enter user id to generate EgoNet: ")

def get_ego_net_features(fp):
    data = dict()
    for line in fp: #iterate for line in file
        line = line.split() #make line into a list
        feature_name = line[1].replace(";anonymized", "") #remove extra stuff
        feature_name = feature_name.replace(";id", "")
        feature_name = feature_name.replace(";", "_")
        
        data[int(line[0])] = (feature_name, line[3]) #append to dict
    return data #return dict

    '''
    takes a file pointer
    returns features in a dictionary
    '''

def add_ego_net_features_to_ego(ego, ego_feature_file, ego_net_features):
    '''Reads a one-line file of features for the ego node'''
    line_list = ego_feature_file.readline().split()    # read one line
    # i is the index, digit is the value
    for i,digit in enumerate(line_list):
        # in order to add a feature we must create a Feature instance
        ego.add_feature(i,Feature(ego_net_features[i][1],
                                  ego_net_features[i][0],int(digit)))
    return ego

def add_alters_to_ego_net(ego_net,alter_features_file,ego_net_features):
    for line in alter_features_file:# for each line in file iterate
        line = line.split() #create a line list from line
        node = Node(int(line[0]), int(len(line)-1))
        
        for i,digit in enumerate(line): #same as given loop in previous func
            if int(digit) > 1:
                continue
            node.add_feature(i-1,Feature(ego_net_features[i-1][1],
                                         ego_net_features[i-1][0],int(digit)))
        
        ego_net.add_alter_node(node) #add alter node to ego
    return ego_net #return updated ego_net

    '''
    takes ego_net, file, and features dictionary as arguments
    adds alters from file to ego net
    returns updated ego_net
    '''


def add_connections_to_ego_net(ego_net,connections_file):
    for line in connections_file: #iterate
        line = line.split() #create line list
        a1 = ego_net.get_alter_node(int(line[0])) #get the alters
        a2 = ego_net.get_alter_node(int(line[1]))
        ego_net.add_connection_between_alters(a1, a2) #eadd a connect
    return ego_net

    '''
    takes an alter connections file
    finds connections and adds them to the egonet
    returns updated egonet
    '''

def add_circles_to_ego_net(ego_net,circles_file):
    for line in circles_file: #iterate
        line = line.split() #list
        name = str(line[0]) #get name
        alters = set() #declare set
        for node_id in line: #iterate through lit
            if not node_id.isdigit(): #make node_id is a number
                continue
            node = ego_net.get_alter_node(int(node_id)) #get node
            alters.add(node) #add node to set
        ego_net.add_circle(name, alters) #add circle to ego net
    return ego_net
    
    '''
    takes the ego net and circle file
    creates circles from file
    returns updated ego net
    '''

def calculate_circle_similarity(ego_net,circle_name):
    circle_dict = dict() #declare dict
    features = ego_net.get_ego_net_features()
    for key in features: #set dict keys to feature positional keys
        circle_dict[key] = []
        
    circ = ego_net.get_circle(circle_name) #get circle from circle egonet
    alters = circ.get_alters() #get alters from ego net
    
    for key in circle_dict: #for every key in the dict we made
        pos = key #feature position
        total = 0 #total of features
        for alter in alters:
            val = alter.get_feature_value(pos)
            total += val
        circle_dict[key] = total #set the feature equal to its total
    
    return circle_dict 

    '''
    takes ego_net and the name of a specific circle
    calculates the totals of specific positions for the circle
    returns a dictionary of the data
    '''
        
def calculate_ego_E_I_index(ego_net,feature_name,feature_id):
    internal = 0 #1 values
    external = 0 #0 values
    alters = ego_net.get_alters() #get the alters
    pos = ego_net.get_feature_pos(feature_name, int(feature_id)) #feature pos
    length = len(alters) #length of alters for equation
    for alter in alters: #increment through each node
        
        val = alter.get_feature_value(pos)

        if val == 1:
            internal += 1 #increment accordingly
        else:
            external += 1
            
    return (external-internal)/length #calculate ei index and return

    '''
    takes ego_net, feature name and feature id as arguments
    calculates EI index of specific feature 
    returns ei index
    '''
            
    
    pass

def calculate_ego_net_effective_size(ego_net):
    count = ego_net.get_alter_node_count() #get count of total nodes
    alters = ego_net.get_alters() #get all alters
    total_alters = len(alters) #get total amount of alters
    redundancy = 0 #declare redundancy to 0
    for alter in alters:
        #total connections -1 because of ego
        connects = len(ego_net.get_alter_connections(alter))-1
        redundancy += connects #get redundancy
    return count-(redundancy/total_alters) #formula

    '''
    takes the ego net
    calculates effective size
    returns effective size
    '''

def calculate_ego_net_efficiency(ego_net):
    effsize = calculate_ego_net_effective_size(ego_net) #effective size
    total_alters = ego_net.get_alter_node_count() #total alters in net
    return effsize/total_alters #formula

    '''
    takes the ego net
    calculates the efficiency of ego net
    returns efficiency of ego net
    '''

def print_choices():
    print("Choices for Ego Net calculation: ")
    print("1 - Top 5 similar features in a circle")
    print("2 - Calculate effective size of Ego Net")
    print("3 - Calculate circle E/I index")
    print("4 - Calculate Ego Net efficiency")
    print("q/Q - Quit ")

def main():
    ego_id,ego_feature_file,ego_net_features_file,alter_features_file,connections_file,circles_file=get_ego_net_files()
    ego_net_features = get_ego_net_features(ego_net_features_file)

    ego = Node(ego_id,len(ego_net_features))

    ego = add_ego_net_features_to_ego(ego,ego_feature_file,ego_net_features)

    FacebookNet = EgoNet(ego,ego_net_features)

    FacebookNet = add_alters_to_ego_net(FacebookNet,alter_features_file,ego_net_features)

    FacebookNet = add_connections_to_ego_net(FacebookNet,connections_file)

    FacebookNet = add_circles_to_ego_net(FacebookNet,circles_file)

    while True:
        print_choices()
        choice = input("Enter choice: ").strip()
        circle_names = FacebookNet.get_circle_names()
        if choice == "1":
            circle_name = input("Enter circle name to calculate similarity: ")
            circle_size = (FacebookNet.get_circle(circle_name).get_circle_size())
            if circle_name in circle_names:
                similarity_dict = calculate_circle_similarity(FacebookNet,circle_name)
            else:
                print("Circle name not in Ego Net's circles. Please try again!")
                continue
            similarity_dict = dict(sorted(similarity_dict.items(),key=itemgetter(1),reverse=True)[:5])
            for feature_pos in similarity_dict:
                feature_name_id = FacebookNet.get_ego_net_feature(feature_pos)
                feature_similarity = (similarity_dict[feature_pos])/(circle_size)
                print(f"Feature: {feature_name_id}")
                print(f"Feature Similarity in {circle_name}: {feature_similarity} \n")
            print()
        elif choice == '2':
            print(f"Effective size of the Ego Net is: {calculate_ego_net_effective_size(FacebookNet)}")
            print()
        elif choice == '3':
            feature_name = input("Enter feature name to calculate E/I index: ")
            feature_id = (input(f"Enter id for {feature_name} to calculate E/I index: "))
            e_i_index = calculate_ego_E_I_index(FacebookNet,feature_name,feature_id)
            if e_i_index < 0:
                print(f"Ego is more homophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()
            else:
                print(f"Ego is more heterophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()

        elif choice == '4':
            ego_net_efficiency = calculate_ego_net_efficiency(FacebookNet)
            print("The efficiency of the Ego Net is: {:.2f}%".format(100*ego_net_efficiency))
            print()

        elif choice in 'qQ':
            break
        else:
            print("Incorrect Choice. Please try again.")
            continue
    ego_feature_file.close()
    ego_net_features_file.close()
    alter_features_file.close()
    connections_file.close()

if __name__ == "__main__":
   main()
