import xml.etree.cElementTree as ET
from datetime import datetime


def add_static_urls(root, url):
    url_element = ET.SubElement(root,"url")
    loc_element = ET.SubElement(url_element, "loc")
    last_mod_element = ET.SubElement(url_element, "lastmod")
    loc_element.text = url
    last_mod_element.text = datetime.date().to_string()

def generate_sitemap():

    schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    #add static pages here
    

    root = ET.Element("urlset")
    # root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    # root.attrib['xsi:schemaLocation'] = schema_loc
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    tree = ET.ElementTree(root)
    tree.write("sitemap.xml",encoding='utf-8', xml_declaration=True)
generate_sitemap()