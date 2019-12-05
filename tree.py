class node:

    def __init__(self, member_info):
        self.left = None
        self.right = None
        self.member_info = member_info

    #Insert new member to the tree
    def insert(self, member_info):
        if self.member_info:
            depth = len(self.member_info["Yakınlık Derecesi"].split())
            if self.member_info["Yakınlık Derecesi"] == "Kendisi":
                depth = 0
            print("Depth:" + str(depth))
            strings = member_info["Yakınlık Derecesi"].split()
            print(strings)
            string = strings[depth]
            print(string)
            if "Anne" in string:
                if self.left is None:
                    self.left = node(member_info)
                else:
                    self.left.insert(member_info)
            elif "Baba" in string:
                if self.right is None:
                    self.right = node(member_info)
                else:
                    self.right.insert(member_info)
        else:
            self.member_info = member_info

    #Inorder print
    def print_tree(self):
        if self.left:
            self.left.print_tree()
        self.print_info()
        if self.right:
            self.right.print_tree()

    #Prints family member details
    def print_info(self):
        print(self.member_info["Yakınlık Derecesi"])