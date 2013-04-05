from lxml import etree


def prepare_card_xml(name, description=None):
    """prepare xml for adding card"""

    def add_propertie(root, name, value):
        """help function to add properties"""

        branch = etree.SubElement(root, 'property')

        br_name = etree.SubElement(branch, "name")
        br_name.text = name
        br_value = etree.SubElement(branch, "value")
        br_value.text = value

    card = etree.Element('card')

    card_name = etree.SubElement(card, "name")
    card_name.text = name

    if description is not None:
        card_descr = etree.SubElement(card, "description")
        card_descr.text = description

    card_type = etree.SubElement(card, "card_type_name")
    card_type.text = "story"

    card_properties = etree.SubElement(card, "properties", type="array")

    add_propertie(card_properties, 'Author', 'svitko')
    add_propertie(card_properties,
                  'Iteration - Scheduled',
                  '(Current Iteration)')

    return etree.tostring(card, pretty_print=True, encoding='UTF-8')
