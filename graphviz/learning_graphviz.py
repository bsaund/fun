from graphviz import Digraph


def first_graph():
    dot = Digraph(comment='The Round Table', engine='neato')
    dot.node('A', 'King Arthur', pos='1,2!')
    dot.node('Bc', 'Sir Bedevere the Wise', pos='2,2.5!')
    dot.node('L', 'Sir Lancelot the Brave', pose='0,0!')

    dot.edges([('A', 'Bc'), 'AL'])
    dot.edge('Bc', 'L', constraint='false')

    print(dot.source)
    dot.render('visuals/round-table.gv', view=True)


def family_graph():
    dot = Digraph(comment='The Round Table', engine='neato')
    dot.node('brad', 'Brad', pos='1,2!')
    dot.node('katie', 'Katie', pos='2,2.5!')
    dot.node('kevdog', 'Kevin', pose='0,0!')

    # dot.edges([('A', 'Bc'), 'AL'])
    dot.edge('brad', 'kevdog', constraint='false')
    dot.edge('katie', 'kevdog', constraint='false')

    print(dot.source)
    dot.render('visuals/family.gv', view=True)


if __name__ == "__main__":
    # first_graph()
    family_graph()
