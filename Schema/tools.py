import rich
from strawberry.types import Info


def extract_subfields(selection, name_atr):
    subfield = {name_atr: []}
    for sub_selection in selection.selections:
        if sub_selection.selections:
            subfield[name_atr].append(getattr(sub_selection, name_atr))
        else:
            subfield[name_atr].append(getattr(sub_selection, name_atr))

    return subfield


def extract_fields(query_fields):
    fields = []

    for field in query_fields.selected_fields:
        for selection in field.selections:
            if hasattr(selection, 'name'):
                if selection.selections:
                    subfield = extract_subfields(selection, 'name')
                    fields.append(subfield)
                else:
                    fields.append(selection.name)
            elif hasattr(selection, 'type_condition'):
                fields.append(selection.type_condition)

    return fields


def card_fields_selected(info: Info):
    fields = []

    result_condition = [select for field in info.selected_fields for select in field.selections
                        if hasattr(select, 'type_condition') if select.type_condition == 'BookObjectResult']

    if result_condition:
        result_condition = result_condition[0].selections

    card_selections = [field for field in result_condition if field.name == 'cards']

    if card_selections:
        card_selections = card_selections[0].selections

    card_sections = [field for field in card_selections if field.name == 'sections']

    if card_sections:
        card_sections = card_sections[0].selections

    for section in card_sections:
        if section.type_condition == 'AbsoluteContainer':
            section_elements = [field for field in section.selections if field.name == 'elements']

            if section_elements:
                section_elements = section_elements[0].selections

            fields.append({section.type_condition: [section.type_condition for section in section_elements]})

        else:
            fields.append(section.type_condition)

    return fields
