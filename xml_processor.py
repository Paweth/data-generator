# import xml.etree.ElementTree as ET
from lxml import etree as ET
import copy

from typing import *

from database_context import *

def get_singular_form(name: AnyStr):
    if name.endswith("ies"):
        return name.replace("ies", "y")
    elif name.endswith("ees"):
        return name.replace("yees", "yee")
    elif name.endswith("ses"):
        return name.replace("ses", "s")
    else:
        return name.removesuffix("s")

def get_column(table : Table, name):
    current_name = ""
    for column in table.columns:
        current_name = column.name
        if column.name.lower() == name.lower():
            return column
    raise Exception(f"No column of that name: {name} in table {table.name}")

class XmlProcessor():
    @classmethod
    def build_tree(cls, db_context : DatabaseContext):
        stack = []
        tree = ET.ElementTree(ET.Element("data"))
        current_root = tree.getroot()
        # root.tag = "data"
        for table in db_context.database.tables:
            row_name = ""
            element = ET.SubElement(current_root, table.name)
            query = f"select * from {table.name}"
            rows, _, description = db_context.get_query_description(query)
            column_labels = [x[0] for x in description]
            if "_" in table.name:
                row_name = "_".join([get_singular_form(row) for row in table.name.split("_")])
            else:
                row_name = get_singular_form(table.name)
            stack.append(current_root)
            current_root = element
            for row in rows:
                element = ET.SubElement(current_root, row_name)
                stack.append(current_root)
                current_root = element
                for i, column_value in enumerate(row):
                    column_name = column_labels[i]
                    column = get_column(table, column_name)
                    if column.constraint != Constraint.PKEY:
                        element = ET.SubElement(current_root, column_name)
                        element.text = str(column_value)
                    else:
                        current_root.set("id", str(column_value))
                    if column.constraint == Constraint.FKEY:
                        element.set("references", f"{column.referenced_table().name}")
                current_root = stack.pop()
            current_root = stack.pop()
        return tree

    @classmethod
    def replace_foreign_keys(cls, db_context : DatabaseContext, tree, level = 0):
        replacements = []
        original_tree = tree
        nested_tree = copy.deepcopy(original_tree)
        root = nested_tree.getroot()
        references = root.findall(".//*[@references]")
        print(f"LENGTH: {len(references)}")
        for reference in references:
            value = reference.text
            referenced_table = reference.get("references")
            element = original_tree.find(f".//{referenced_table}/*[@id='{value}']")
            if element is not None:
                replacements.append((reference, element))
            else:
                print(f"No element of id: {value} in {referenced_table}")
        for reference, new_element in replacements:
            parent = reference.getparent()
            index = list(parent).index(reference)
            parent[index] = copy.deepcopy(new_element)
        return nested_tree

    @classmethod
    def write_to_file(cls, tree, path):
        ET.indent(tree)
        tree.write(path)
        # tree.write("./xml/output.xml")

    @classmethod
    def convert_database_to_xml(cls, db_context, level, path):
        tree = XmlProcessor.build_tree(db_context)
        XmlProcessor.write_to_file(tree, path)

    @classmethod
    def write_nested(cls, db_context : DatabaseContext, level = 0):
        #search columns from query in db_context and get dependency info to perform substitution
        stack = []
        tree = ET.ElementTree(ET.Element("data"))
        current_root = tree.getroot()
        # root.tag = "data"
        for table in db_context.database.tables:
            row_name = ""
            # element = ET.Element({table.name})
            element = ET.SubElement(current_root, table.name)
            rows, _, description = db_context.get_query_description(f"select * from {table.name}")
            # prepare data for foreign_key substitution (build multi-level data structure?)
            print(f"DESCRIPTION: {description}")
            # print(description[0][1])
            column_labels = [x[0] for x in description]
            print(f"LABELS: {column_labels}")
            if "_" in table.name:
                row_name = "_".join([get_singular_form(row) for row in table.name.split("_")])
            else:
                row_name = get_singular_form(table.name)

            stack.append(current_root)
            current_root = element
            for row in rows:
                element = ET.SubElement(current_root, row_name)
                stack.append(current_root)
                current_root = element
                # recurrent here / seperate to function
                for i, column_data  in enumerate(row):
                        column_name = column_labels[i]
                        col = get_column(table, column_name)
                        if col.constraint == Constraint.FKEY:
                            referenced_table = col.referenced_table()
                            query = f"select * from {referenced_table.name} where id = {column_data}"
                            print(query)
                            foreign_rows, _, f_description = db_context.get_query_description(query) # change so outside it would search once (or get from xml? - data is already read)
                            f_column_labels = [x[0] for x in f_description]

                            element = ET.SubElement(current_root, get_singular_form(referenced_table.name))
                            stack.append(current_root)
                            current_root = element
                            for i, f_column_data in enumerate(foreign_rows[0]):
                                f_column_name = f_column_labels[i]
                                element = ET.SubElement(current_root, f_column_name)
                                element.text = str(f_column_data)
                            current_root = stack.pop()
                        else:           
                            print(f"{col.name}: {column_data}")
                            element = ET.SubElement(current_root, column_name)
                            element.text = str(column_data)
                current_root = stack.pop()
            current_root = stack.pop()
        # XmlProcessor.print_tree(tree.getroot())
        ET.indent(tree)
        # cls.indent(tree.getroot())
        tree.write("./xml/output.xml")

    @classmethod
    def read(cls, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    
    @classmethod
    def print_tree(cls, root, level = 0):
        for child in root:
            print(f"{"".join(["  " for _ in range(level)])}{child.tag}")
            cls.print_tree(child, level + 1)

def test_xml():
    db_context = DatabaseContext()
    original_tree = XmlProcessor.build_tree(db_context)
    nested_tree = XmlProcessor.replace_foreign_keys(db_context, original_tree)
    XmlProcessor.write_to_file(nested_tree, "./xml/output.xml")

if __name__ == "__main__":
    test_xml()