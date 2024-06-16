import argparse
import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

words_list=[]
words_to_id={}
id_to_words={}
global graph_matrix

    
def showDirectedGraph(id_to_words, path=None, distance=None, show_path=False):
    
    
    G = nx.from_numpy_array(graph_matrix, create_using=nx.DiGraph)
    H = nx.relabel_nodes(G, id_to_words)
    pos = nx.spring_layout(H,seed=7)  # 生成节点位置

    # 绘制基本图形
    nx.draw(H, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=700)
    
    if show_path:
        # 高亮路径
        path_edges=[]
        for i in range(len(path)-1):
            path_edges.append((id_to_words[path[i]],id_to_words[path[i+1]]))
        #path_edges = list(zip(path, path[1:]))
        #print(path_edges)
        nx.draw_networkx_edges(H, pos, edgelist=path_edges, edge_color='red', width=2, arrowstyle='-|>')
        # 添加最短路径长度注释
        plt.text(0.05, 0.95, f'the length of the shortest way:{distance}', transform=plt.gcf().transFigure, fontsize=12)

    # 显示边的权重
    edge_labels = nx.get_edge_attributes(H, 'weight')
    #print(pos)
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels)
    # 显示图形
    plt.show()

def queryBridgeWords(word1,word2,default=False):
       
    if word1 not in words_to_id and word2 not in words_to_id:
        if default:
            return []
        return f"No \"{word1}\" and \"{word2}\" in the graph!"
    elif  word1 not in words_to_id:
        if default:
            return []
        return f"No \"{word1}\" in the graph!"
    elif  word2 not in words_to_id:
        if default:
            return []
        return f"No \"{word2}\" in the graph!"
    x=words_to_id[word1]
    y=words_to_id[word2]
    num = graph_matrix.shape[0]
    ans=[]
    for i in range(num):
        if graph_matrix[x][i] and graph_matrix[i][y]:
            ans.append(id_to_words[i])
    if default:
        return ans
    if not ans:
        return f"No bridge words from \"{word1}\" to \"{word2}\"!"
    output=f"The bridge words from \"{word1}\" to \"{word2}\" "
    inter_num=len(ans)
    if inter_num==1:
        output +=f"is: {ans[0]}"
        return output
    output+="are: "
    for i in range(inter_num-1):
        output+=ans[i]
        output+=", "
    output +=f"and {ans[inter_num-1]}"
    return output
    
    
def generateNewText(sentence):
    new_words_list = re.findall(r'\b\w+\b', sentence) 
    new_lenth = len(new_words_list)
    p = 1
    combine_word = []
    combine_word.append(new_words_list[0])
    while p<new_lenth:
        out = queryBridgeWords(new_words_list[p-1],new_words_list[p],True)
        if out == []:
            combine_word.append(new_words_list[p])
            p += 1
            continue
        item = random.choice(out)
        combine_word.append(item)
        combine_word.append(new_words_list[p])
        p += 1
    out_sentence = ""
    for i in combine_word:
        out_sentence += (i+" ")
    return out_sentence.strip()
        
def get_next(idx):
    length = len(words_to_id)
    out = []
    for i in range(length):
        if graph_matrix[idx][i] == 0:
            continue
        out.append(i)
    
    if out == []:
        return "-"
    return random.choice(out)

def randomWalk():
    p = random.randint(0, len(words_to_id)-1)
    record = []
    out = []
    out.append(id_to_words[p])
    next = get_next(p)
    if next == "-":
        return out[0]
    record_line = str(p)+"-"+str(next)
    while record_line not in record:
        out.append(id_to_words[next])
        record.append(record_line)
        p = next
        next = get_next(p)
        if next == "-":
            break
        record_line = str(p)+"-"+str(next)
    if next != "-":
        out.append(id_to_words[next])
    out_sentence = ""
    for i in out:
        out_sentence += (i+" ")
    return out_sentence.strip()
    
def dijkstra_all(src, num):
    new_matrix=np.copy(graph_matrix)
    #np.fill_diagonal(new_matrix, -np.inf)
    new_matrix[new_matrix == 0] = np.inf
    #np.fill_diagonal(new_matrix, 0)
    distances = [float('inf')] * num  # 距离数组，初始化为无穷大
    #print(new_matrix)
    distances[src] = 0  # 源点到自己的距离是0
    visited = [False] * num  # 访问数组，初始化为未访问
    all_paths={}
    #for i in range(num):
    #    all_paths[i]=[]
    all_paths = {i: [] for i in range(num)}  # 使用字典来存储到每个节点的所有路径
    all_paths[src].append([src])  # 源到自己的路径

    while True:
        # 选择一个未访问的顶点，具有最小距离
        min_distance = float('inf')
        min_idx = -1
        for v in range(num):
            if distances[v] < min_distance and not visited[v]:
                min_distance = distances[v]
                min_idx = v

        if min_idx == -1:
            break

        # 标记这个顶点为已访问
        visited[min_idx] = True

        # 更新所有邻接的未访问顶点的距离和路径
        for v in range(num):
            if new_matrix[min_idx][v] != float('inf'):
                distance = distances[min_idx] + new_matrix[min_idx][v]
                if distance < distances[v]:
                    distances[v] = distance
                    all_paths[v] = [path + [v] for path in all_paths[min_idx]]
                elif distance == distances[v]:  # 这里处理多条最短路径的情况
                    all_paths[v].extend([path + [v] for path in all_paths[min_idx]])
    #print(distances,all_paths)

    return distances, all_paths

def calcShortestPath(num,word1,word2,one_word,show_all):
    u=words_to_id[word1]
    distances,all_paths=dijkstra_all(u,num)
    print(all_paths)
    if one_word:
        if show_all:
            for paths,dist in zip(all_paths,distances):
                if all_paths[paths]==[]:
                    print(f"It's impossible to reach {id_to_words[paths]} from {word1}")
                else:
                    for path in all_paths[paths]:
                        showDirectedGraph(id_to_words,path,dist,True)
            return 
        else:
            for paths,dist in zip(all_paths,distances):
                if all_paths[paths]==[]:
                    print(f"It's impossible to reach {id_to_words[paths]} from {word1}")
                else:
                    showDirectedGraph(id_to_words,all_paths[paths][0],dist,True)
            return
    else:
        v=words_to_id[word2]
        dist=distances[v]
        paths=all_paths[v]
        if paths==[]:
            print(f"It's impossible to reach {word2} from {word1}")
            return 
        if show_all:
            for path in paths:
                showDirectedGraph(id_to_words,path,dist,True)
            return
        else:
            showDirectedGraph(id_to_words,paths[0],dist,True)
            return   
        
    
def load_data(file_path):
    global words_list
    with open(file_path, 'r') as file:
        text = file.read().lower()  
        words_list = re.findall(r'\b\w+\b', text)
    length=len(words_list)
    idx=0
    for i in words_list:
        if i not in words_to_id:
            words_to_id[i]=idx
            id_to_words[idx]=i
            idx+=1
    return length,idx

def get_args_parser():
    parser = argparse.ArgumentParser('LAB1', add_help=False)
    parser.add_argument('--file_path', default="text.txt", type=str)
    return parser
        
if __name__ == '__main__':
    args = get_args_parser()
    args = args.parse_args()
    if not args.file_path:
        args.file_path=input("please input your file path:")
    length,num = load_data(args.file_path)
    
    graph_matrix=np.zeros((num,num))

    for i in range(length-1):
        x=words_list[i]
        y=words_list[i+1]
        graph_matrix[words_to_id[x]][words_to_id[y]]+=1
    
    while(True):
        print("hi")
        print("choose a number")
    
        case = int(input("choose(show:1,query:2,generate:3,calculate:4,random:5):"))
        
        # sentence = "Seek to explore new and exciting synergies"
        # print(generateNewText(sentence))
        if case==1:
            showDirectedGraph(id_to_words)
        if case==2:
            word1 = input("word1:").lower()
            word2 = input("word2:").lower()
            print(queryBridgeWords(word1,word2))
        if case==3:
            sentence = input("sentence:")
            print(generateNewText(sentence))
        if case==4:
            one_word=bool(input("one_word:"))
            word1 = input("begin:").lower()
            if not one_word:
                word2 = input("end:").lower()
            show_all=bool(input("show_all:"))
            if not one_word:
                calcShortestPath(num,word1,word2,one_word,show_all)
            else:
                calcShortestPath(num,word1,"",one_word,show_all)
        if case==5:
            print(randomWalk())


    
    

    
        

