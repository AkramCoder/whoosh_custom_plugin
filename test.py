from whoosh import qparser


class CustomPlugin(qparser.plugins.Plugin):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def filters(self, parser):
        # Run after the fields filter applies explicit fieldnames (at priority
        # 100)
        return [(self.generate_new_nodes, 110)]

    def generate_new_nodes(self, parser, group):
        terms = ['ملوك', 'ملك', 'ملكة']
        newgroup = group.empty_copy()

        for i, node in enumerate(group):
            print("node", node)
            if node.has_fieldname:
                if node.has_text:
                    if node.text == 'ملك':
                        for term in terms:
                            newnode = qparser.WordNode(term)
                            newnode.set_fieldname(self.fieldname)
                            newnode.startchar = node.startchar
                            newnode.endchar = node.endchar
                            newgroup.append(newnode)
                    else:
                        newnode = qparser.WordNode(node.text)
                        newnode.set_fieldname(self.fieldname)
                        newnode.startchar = node.startchar
                        newnode.endchar = node.endchar
                        newgroup.append(newnode)
        return newgroup


qp = qparser.QueryParser("content", schema=None)
qp.add_plugin(CustomPlugin(qp.fieldname))
q = qp.parse(u"اكل ملك")
print(q)
