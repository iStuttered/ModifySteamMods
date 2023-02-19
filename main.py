import argparse, os, pathlib
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from loguru import logger


def make_element_at_path(xml_tree: Element, element_path: str, element_value):
    sections = element_path.split('/')

    section = sections[0]

    if len(sections) == 1:
        section_element = xml_tree.find(section)
        if section_element is None:
            xml_tree.append(Element(section))
            xml_tree.find(section).text = element_value
        else:
            section_element.text = element_value
        return
    else:
        if xml_tree.find(section) is None:
            xml_tree.append(Element(section))

        make_element_at_path(xml_tree.find(section), '/'.join(sections[1:]), element_value)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("property")
    parser.add_argument("value")
    parser.add_argument('-f', "--folder", default="C:/Program Files (x86)/Steam/steamapps/workshop/content/289070",
                        required=False)

    args = parser.parse_args()

    mods_folder = args.folder
    property_path = args.property
    property_value = args.value

    for folder in os.listdir(mods_folder):
        absolute_folder_path = os.path.join(mods_folder, folder)
        mod_info_path = sorted(pathlib.Path(absolute_folder_path).glob('*.modinfo'))[0]
        mod_info_xml = ElementTree.parse(mod_info_path)
        mod_info_xml_root = mod_info_xml.getroot()
        mod_name = mod_info_xml_root.find("./Properties/Name").text

        xml_property = mod_info_xml.find(property_path)
        make_element_at_path(mod_info_xml_root, property_path, property_value)
        mod_info_xml.write(mod_info_path, xml_declaration=True, encoding='utf-8')

        logger.info(f"Updated {mod_name}: {property_path} -> {property_value}")
