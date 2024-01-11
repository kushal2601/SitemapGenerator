import xml.etree.cElementTree as ET
'''
Create one main sitemap_index.xml
    <sitemap>
        <loc>http://mycareers.net/sitemap/static/static_sitemap.xml</loc>
    </sitemap>
    <sitemap>
        <loc>http://mycareers.net/sitemap/dynamic/sitemap1.xml</loc>
    </sitemap>
    <sitemap>
        <loc>http://mycareers.net/sitemap/dynamic/sitemap2.xml</loc>
    </sitemap>
'''

def generate_sitemap(fileName):

    # schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
    #               "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    root = ET.Element("urlset")

    # root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    # root.attrib['xsi:schemaLocation'] = schema_loc
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    tree = ET.ElementTree(root)
    tree.write(fileName,encoding='utf-8', xml_declaration=True)
    return root
# generate_sitemap("sitemap0.xml")
def get_url_element(url):
    root = ET.Element("url")    
    loc_element = ET.SubElement(root, "loc")
    loc_element.text = url

    return root
def get_sitemap_element(fileName):
    root = ET.Element("sitemap")
    loc_element = ET.SubElement(root, "loc")
    loc_element.text = fileName

    return root