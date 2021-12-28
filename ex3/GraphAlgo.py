import collections
import math
import time
from typing import List
import sys
import json
import DiGraph
from src import GraphAlgoInterface
from src import GraphInterface
from itertools import permutations
from collections import defaultdict, Counter
import copy
import tkinter
from tkinter import *
import random

class GraphAlgo(GraphAlgoInterface.GraphAlgoInterface):

    def __init__(self, g: GraphInterface.GraphInterface = DiGraph.DiGraph()):
        self.g = g
        self.shortest_path_dict = defaultdict(list)

    def get_graph(self) -> GraphInterface:
        return self.g

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.g = DiGraph.DiGraph()
            f = open(file_name)
            data = json.load(f)
            Edges = data.get("Edges")
            Nodes = data.get("Nodes")
            for n in Nodes:
                pos = n.get("pos")
                new_pos = pos.split(",")
                self.g.add_node(n.get("id"), (new_pos[0], new_pos[1]))
            for e in Edges:
                self.g.add_edge(e.get("src"), e.get("dest"), e.get("w"))
            return True
        except FileNotFoundError:
            return False

    def save_to_json(self, file_name: str) -> bool:

        Nodes = self.g.get_all_v()
        new_Nodes = []
        for n in Nodes:
            new_n = Nodes.get(n)
            st = new_n.getPos()
            st1 = st[0] + "," + st[1] + ",0.0"
            list_n = {}
            list_n["pos"] = st1
            list_n["id"] = n
            new_Nodes.append(list_n)

        Edges = self.g.get_all_edges()
        new_Edges = []
        for e in Edges:
            list_e = {}
            list_e["src"] = e.get_src()
            list_e["w"] = e.get_weight()
            list_e["dest"] = e.get_dest()
            new_Edges.append(list_e)
        new_graph = {}
        new_graph["Edges"] = new_Edges
        new_graph["Nodes"] = new_Nodes

        try:
            with open(file_name, 'w') as outfile:
                json.dump(new_graph, outfile)
                return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        id_weight = {}
        id_previous = {}
        unvisited = list(self.g.get_all_v().keys())
        visited = []
        for n in self.g.get_all_v():
            if n == id1:
                id_weight[n] = 0
            else:
                id_weight[n] = sys.float_info.max

        while unvisited:
            current_vertex = min(unvisited, key=id_weight.get)
            neighbours = self.g.all_out_edges_of_node(current_vertex)
            for n in neighbours:
                path_weight = float(neighbours[n]) + id_weight[current_vertex]
                if path_weight < id_weight[n]:
                    id_weight[n] = path_weight
                    id_previous[n] = current_vertex
            unvisited.remove(current_vertex)
            visited.append(current_vertex)

        self.shortest_path_dict[id1].append(id_weight)
        self.shortest_path_dict[id1].append(id_previous)
        if not id_previous:
            return -1, []

        w = id_weight[id2]
        path = [id2]
        current_node = id2
        while current_node != id1:
            if current_node in id_previous:
                current_node = id_previous[current_node]
                path.append(current_node)
            else:
                return -1, []

        path = path[::-1]
        return w, path

    def longest_path(self, id1: int) -> float:
        id_weight = {}
        id_previous = {}
        unvisited = list(self.g.get_all_v().keys())
        visited = []
        for n in self.g.get_all_v():
            if n == id1:
                id_weight[n] = 0
            else:
                id_weight[n] = sys.float_info.max

        while unvisited:
            current_vertex = min(unvisited, key=id_weight.get)
            neighbours = self.g.all_out_edges_of_node(current_vertex)
            for n in neighbours:
                path_weight = float(neighbours[n]) + id_weight[current_vertex]
                if path_weight < id_weight[n]:
                    id_weight[n] = path_weight
                    id_previous[n] = current_vertex
            unvisited.remove(current_vertex)
            visited.append(current_vertex)

        return max(id_weight.values())

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        start_end = list(permutations(node_lst, 2))
        best_path = None
        best_path_weight = sys.float_info.max
        for pair in start_end:
            w, p = GraphAlgo.shortest_path(self, pair[0], pair[1])
            check = all(item in p for item in node_lst)
            if w < best_path_weight and check:
                best_path = p
                best_path_weight = w

        if best_path is not None:
            return best_path, best_path_weight

        unvisited = copy.deepcopy(node_lst)
        for n in node_lst:
            unvisited.remove(n)
            best_path1 = [n]
            total_weight = 0
            prev_ver = n
            size = len(unvisited)
            for i in range(size):
                closest_ver = min(unvisited, key=self.shortest_path_dict[prev_ver][0].get)
                w, p = GraphAlgo.shortest_path(self, prev_ver, closest_ver)
                total_weight += w
                best_path1.extend(p[1:])
                unvisited.remove(closest_ver)
                prev_ver = closest_ver

            if total_weight < best_path_weight:
                best_path_weight = total_weight
                best_path = best_path1

            unvisited = copy.deepcopy(node_lst)

        set1 = set(best_path)
        set2 = set(node_lst)

        if set2.issubset(set1):
            return best_path, best_path_weight

        return None, sys.float_info.max

    def centerPoint(self) -> (int, float):
        center = None
        weight = sys.float_info.max
        for n in self.g.get_all_v():
            longest_path = GraphAlgo.longest_path(self, n)
            if longest_path < weight:
                center = n
                weight = longest_path

        return center, weight

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        m = tkinter.Tk()
        m.title("Graph Gui")
        screen_width = m.winfo_screenwidth()
        screen_height = m.winfo_screenheight()
        can = Canvas(m, width=screen_width / 1.5, height=screen_height / 1.5)
        can.pack()
        menubar = Menu(m)
        m.config(menu=menubar)
        load_menu = Menu(menubar)
        menubar.add_cascade(label="Load", menu=load_menu)
        load_menu.add_command(label="load", command=lambda: self.load_f(can, screen_width / 1.5, screen_height / 1.5))

        save_menu = Menu(menubar)
        menubar.add_cascade(label="Save", menu=save_menu)
        save_menu.add_command(label="save", command=lambda: self.save_f())

        edit_menu = Menu(menubar)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="add node",command=lambda: self.add_node_to_graph(can, screen_width, screen_height))
        edit_menu.add_command(label="remove node",command=lambda: self.remove_node_from_graph(can, screen_width, screen_height))
        edit_menu.add_command(label="add edge",command=lambda: self.add_edge_to_graph(can, screen_width, screen_height))
        edit_menu.add_command(label="remove edge",command=lambda: self.remove_edge_from_graph(can, screen_width, screen_height))

        run_menu = Menu(menubar)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="center",command=lambda: self.show_center())
        run_menu.add_command(label="shortest path", command=lambda: self.show_shortest_path())
        run_menu.add_command(label="TSP", command=lambda: self.show_TSP())

        GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)
        m.mainloop()




    def show_TSP(self):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter in this format:id1,id2,id3...", command=lambda: self.send_to_TSP(e))
        b.pack()

    def send_to_TSP(self, e):
        e = e.get()
        l = list(e.split(","))
        node_list = list(map(int, l))
        path, w = self.TSP(node_list)
        msg = f"the shortest path is: {path} with distance of: {w}"
        GraphAlgo.create_window(self, msg)

    def show_shortest_path(self):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter in this format:id1,id2", command=lambda: self.send_to_shortest_path(e))
        b.pack()

    def send_to_shortest_path(self, e):
        e = e.get()
        id1 = e.split(",")[0]
        id2 = e.split(",")[1]
        w, path = self.shortest_path(int(id1), int(id2))
        msg = f"the shortest path is: {path} with distance of: {w}"
        GraphAlgo.create_window(self, msg)

    def show_center(self):
        id1, w = self.centerPoint()
        msg = f"the center point is node: {id1} with min-max distance of: {w}"
        GraphAlgo.create_window(self, msg)

    def remove_edge_from_graph(self, canvas, screen_width, screen_height):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter in this format:id1,id2", command=lambda: self.send_to_remove_edge(e, canvas, screen_width, screen_height))
        b.pack()

    def send_to_remove_edge(self, e, can, screen_width, screen_height):
        e = e.get()
        id1 = e.split(",")[0]
        id2 = e.split(",")[1]
        self.g.remove_edge(int(id1), int(id2))
        can.delete("all")
        GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)

    def add_edge_to_graph(self, canvas, screen_width, screen_height):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter in this format:id1,id2,weight", command=lambda: self.send_to_add_edge(e, canvas, screen_width, screen_height))
        b.pack()

    def send_to_add_edge(self, e, can, screen_width, screen_height):
        e = e.get()
        id1 = e.split(",")[0]
        id2 = e.split(",")[1]
        w = e.split(",")[2]
        self.g.add_edge(int(id1), int(id2), float(w))
        can.delete("all")
        GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)


    def remove_node_from_graph(self, canvas, screen_width, screen_height):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter id of node", command=lambda: self.send_to_remove_node(e, canvas, screen_width, screen_height))
        b.pack()

    def send_to_remove_node(self, e, can, screen_width, screen_height):
        e = e.get()
        self.g.remove_node(int(e))
        can.delete("all")
        GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)

    def add_node_to_graph(self, canvas, screen_width, screen_height):
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="Enter in this format:id,x,y or just the id", command=lambda: self.send_to_add_node(e, canvas, screen_width, screen_height))
        b.pack()

    def send_to_add_node(self, e, can, screen_width, screen_height):
        e = e.get()
        if len(e.split(",")) != 1:
            id = e.split(",")[0]
            pos = (e.split(",")[1], e.split(",")[2])
            self.g.add_node(int(id), pos)
            can.delete("all")
            GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)
        else:
            id = e.split(",")[0]
            self.g.add_node(id, None)
            can.delete("all")
            GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)

    def plot_Graph(self, can, screen_width, screen_height):
        nodes = self.g.get_all_v()
        max_x = 0
        max_y = 0
        min_x = sys.float_info.max
        min_y = sys.float_info.max
        for id, n in nodes.items():
            if n.getPos() is not None:
                x, y = n.getPos()
                x = float(x)
                y = float(y)
                if x < min_x:
                    min_x = x
                elif x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                elif y > max_y:
                    max_y = y

        min_x -= 0.000625
        min_y -= 0.000625
        max_x += 0.000625
        max_y += 0.000625
        nodes_with_pos = []
        nodes_with_no_pos = []
        for id, n in nodes.items():
            if n.getPos() is not None:
                x, y = n.getPos()
                x = float(x)
                y = float(y)
                x = (x - min_x) / (max_x - min_x)
                y = (y - min_y) / (max_y - min_y)
                final_x = int(x * screen_width)
                final_y = int(y * screen_height)
                GraphAlgo.create_circle(self, can, final_x, final_y, id)
                nodes_with_pos.append(n)
            else:
                nodes_with_no_pos.append(n)

        if len(nodes_with_pos) == 0:
            for n in nodes_with_no_pos:
                x = random.uniform(0, 1)
                y = random.uniform(0, 1)
                n.setPos(str(x), str(y))
                x = (x - min_x) / (max_x - min_x)
                y = (y - min_y) / (max_y - min_y)
                final_x = int(x * screen_width)
                final_y = int(y * screen_height)
                GraphAlgo.create_circle(self, can, final_x, final_y, n.getId())
                nodes_with_pos.append(n)

        for n in nodes_with_no_pos:
            x = 0
            y = 0
            num = random.randrange(1, len(nodes_with_pos), 1)
            for i in range(num):
                index = random.randrange(0, len(nodes_with_pos), 1)
                x += float(nodes_with_pos[index].getPos()[0])
            x = x/num
            num = random.randrange(1, len(nodes_with_pos), 1)
            for i in range(num):
                index = random.randrange(0, len(nodes_with_pos), 1)
                y += float(nodes_with_pos[index].getPos()[1])

            y = y / num
            n.setPos(str(x), str(y))
            x = (x - min_x) / (max_x - min_x)
            y = (y - min_y) / (max_y - min_y)
            final_x = int(x * screen_width)
            final_y = int(y * screen_height)
            GraphAlgo.create_circle(self, can, final_x, final_y, n.getId())
            nodes_with_pos.append(n)

        for id, n in nodes.items():
            x, y = n.getPos()
            x = float(x)
            y = float(y)
            x = (x - min_x) / (max_x - min_x)
            y = (y - min_y) / (max_y - min_y)
            final_x = int(x * screen_width)
            final_y = int(y * screen_height)
            edges_from_node = self.g.all_out_edges_of_node(id)
            for e in edges_from_node:
                if e in nodes.keys():
                    dest_x, dest_y = nodes[e].getPos()
                    dest_x = float(dest_x)
                    dest_y = float(dest_y)
                    dest_x = (dest_x - min_x) / (max_x - min_x)
                    dest_y = (dest_y - min_y) / (max_y - min_y)
                    final_dest_x = int(dest_x * screen_width)
                    final_dest_y = int(dest_y * screen_height)
                    GraphAlgo.draw_arrow(self, final_x, final_y, final_dest_x, final_dest_y, 6, 5, can)

    def draw_arrow(self, x1, y1, x2, y2, d, h, canvas):
        dx = x2 - x1
        dy = y2 - y1
        D = math.sqrt(dx * dx + dy * dy)
        xm = D - d
        xn = xm
        ym = h
        yn = -h
        sin = dy / D
        cos = dx / D
        x = xm * cos - ym * sin + x1
        ym = xm * sin + ym * cos + y1
        xm = x
        x = xn * cos - yn * sin + x1
        yn = xn * sin + yn * cos + y1
        xn = x
        points = [x2, y2, int(xm), int(ym), int(xn), int(yn)]
        canvas.create_line(x1, y1, x2, y2)
        canvas.create_polygon(points, fill="black")

    def create_circle(self, canvas, x, y, id_node):
        x0 = x - 10
        y0 = y - 10
        x1 = x + 10
        y1 = y + 10
        canvas.create_text(x0-5, y0-5, text=str(id_node))
        return canvas.create_oval(x0, y0, x1, y1, fill="red")

    # a function that gets the input un the entry, cleans it, and try to save the graph to the input given,
    # and calls for a window to give response if it succeded or not
    def try_save(self, e) -> None:
        new_e = e.get()
        e.delete(0, 'end')
        flag = self.save_to_json(new_e)
        if not flag:
            self.create_window("the entry you gave was inadequate, please try again")
        else:
            self.create_window("the file was saved!")

    # create a window to which we put the input of the file we want to save the graph to
    def save_f(self) -> None:
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="enter the name of the file you want to save to:", command=lambda: self.try_save(e))
        b.pack()

    def load_f(self, canvas, screen_width, screen_height) -> None:
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        e = Entry(w)
        e.pack()
        b = Button(w, text="enter the path/name of the file you want to load:", command=lambda: self.try_load(e, canvas, screen_width, screen_height))
        b.pack()

    def try_load(self, e, can, screen_width, screen_height) -> None:
        new_e = e.get()
        e.delete(0, 'end')
        flag = self.load_from_json(new_e)
        if not flag:
            self.create_window("the entry you gave was inadequate, please try again")
        else:
            self.create_window("the file was loaded to the graph!")
            can.delete('all')
            GraphAlgo.plot_Graph(self, can, screen_width / 1.5, screen_height / 1.5)

    def create_window(self, st) -> None:
        w = Tk()
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        can = Canvas(w, width=screen_width / 5, height=screen_height / 5)
        can.pack()
        l1 = Label(w, text=st)
        l1.pack()

