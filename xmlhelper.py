from lxml import etree
import base64
import logging


def prepare_card_xml(name, description=None, properties=None):
    """prepare xml for adding card"""

    def add_propertie(root, name, value):
        """help function to add properties"""

        branch = etree.SubElement(root, 'property')

        br_name = etree.SubElement(branch, "name")
        br_name.text = name
        br_value = etree.SubElement(branch, "value")
        br_value.text = str(value)

    card = etree.Element('card')

    card_name = etree.SubElement(card, "name")
    card_name.text = name

    if description is not None:
        card_descr = etree.SubElement(card, "description")
        card_descr.text = description

    card_type = etree.SubElement(card, "card_type_name")
    card_type.text = "story"

    if properties is not None:
        card_properties = etree.SubElement(card, "properties", type="array")

        for name, value in properties.items():
            logging.debug("adding property {}={} to card {}".format(
                name, value, card_name))
            add_propertie(card_properties, name, value)

    return etree.tounicode(card, pretty_print=True)
