import turtle as ttl
import tkinter as tk

VERTICAL_CHANGE = 120
HORIZONTAL_CHANGE = 50
EDGE_HALF_LENGTH = 30

class node:

    def __init__(self, member_info):
        self.left = None
        self.right = None
        self.member_info = member_info
        self.x = 0
        self.y = 0

    #Insert new member to the tree
    def insert(self, member_info):
        if self.member_info:
            depth = len(self.member_info["Yakınlık Derecesi"].split())
            if self.member_info["Yakınlık Derecesi"] == "Kendisi":
                depth = 0
            strings = member_info["Yakınlık Derecesi"].split()
            string = strings[depth]
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
        print("------------------------------")
        if self.right:
            self.right.print_tree()

    #Prints family member details
    def print_info(self):
        print(self.member_info["Sıra"])
        print(self.member_info["Yakınlık Derecesi"])
        print(self.member_info["Adı"] + " " + self.member_info["Soyadı"])
        print(self.member_info["Doğum Yeri ve Tarihi"])
        print(self.member_info["Durumu"])

    #Draw the lines and create the circles with preorder traversal
    def preorder_draw(self, canvas, turtle):
        #Make text shorter to avoid collision
        text = self.member_info["Adı"]
        text = text.split()[0]
        if len(text) > 6:
            text = text[0:5] + "..."

        #draw lines
        turtle.goto(self.x, self.y)
    
        #draw text just for animation // will be destroyed using the tag
        canvas.create_rectangle(self.x-EDGE_HALF_LENGTH,-(self.y-EDGE_HALF_LENGTH),self.x+EDGE_HALF_LENGTH,-(self.y+EDGE_HALF_LENGTH), fill="white", outline="white", tags="to_be_destroyed")
        canvas.create_text(self.x,-(self.y), text=text, font=("Purisa",(EDGE_HALF_LENGTH/3).__round__(), "bold"), tags="to_be_destroyed")
        if self.left:
            self.left.preorder_draw(canvas, turtle)
        turtle.up()
        turtle.goto(self.x, self.y)
        turtle.down()
        if self.right:
            self.right.preorder_draw(canvas, turtle)
        canvas.create_rectangle(self.x-EDGE_HALF_LENGTH,-(self.y-EDGE_HALF_LENGTH),self.x+EDGE_HALF_LENGTH,-(self.y+EDGE_HALF_LENGTH), fill="white", outline="white", tags=["person", self.member_info["Sıra"]+"_box", "box"])
        canvas.create_text(self.x,-(self.y), text=text, font=("Purisa",(EDGE_HALF_LENGTH/3).__round__(), "bold"), tags=["person", self.member_info["Sıra"], "text"])

    #Inorder traversal to calculate the positions of the nodes
    def calculate_positions(self, x, y):
        y = y - VERTICAL_CHANGE
        if self.left:
            x = self.left.calculate_positions(x, y)
        self.x = x
        self.y = -y
        x = x + HORIZONTAL_CHANGE
        if self.right:
            x = self.right.calculate_positions(x, y)
        return x

    #Inorder traversal to count number of nodes
    def count_tree(self, count):
        if self.left:
            count = self.left.count_tree(count)
        count = count + 1
        if self.right:
            count = self.right.count_tree(count)
        return count

    #Calculate depth by postorder traversal
    def calculate_depth(self):
        left = 0
        if self.left:
            left = self.left.calculate_depth()
        right = 0
        if self.right:
            right = self.right.calculate_depth()
        return 1 + max(left,right)

    #Inorder traversal search to find data by attribute. Returns a list of all matched nodes' data
    def search(self, value, attribute="Sıra", data=[]):
        if self.left:
            data = self.left.search(value, attribute, data)
        if self.member_info[attribute] == value:
            data.append(self.member_info)
        if self.right:
             data = self.right.search(value, attribute, data)
        return data

    def visualize_tree(self, canvas):
        turtle = ttl.RawTurtle(canvas)
        turtle.pencolor("#000000") # Black
        turtle.hideturtle()
        turtle.speed(5)
        count = self.count_tree(0)
        depth = self.calculate_depth()
        #COLLISION AVOIDANCE
        #The code below is meant for the squares which are invisible in the app. The texts shown use EDGE_HALF_LENGTH to approximate font size however this may not work all the time.
        global HORIZONTAL_CHANGE, EDGE_HALF_LENGTH, VERTICAL_CHANGE
        HORIZONTAL_CHANGE = canvas.winfo_width()/(count+1) # the tree will put this amount of horizontal space between each node to avoid collision
        VERTICAL_CHANGE = canvas.winfo_height()/(depth+1) # the tree will put this amount of vertical space between each depth level to avoid collision
        EDGE_HALF_LENGTH = min(HORIZONTAL_CHANGE/2, VERTICAL_CHANGE/2) #pick smallest dimension to avoid collision
        self.calculate_positions(canvas.canvasx(0 + HORIZONTAL_CHANGE), canvas.canvasy(canvas.winfo_height())) #calculate the positions of the nodes to avoid collision
        turtle.up()
        turtle.goto(self.x, self.y) #start drawing from root.
        turtle.down()
        self.preorder_draw(canvas,turtle) #draw the tree and nodes
        canvas.delete("to_be_destroyed") #get rid of nodes created for animation