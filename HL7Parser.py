from ParsedMessage import ParsedMessage
from HL7Segment import HL7Segment


def parse(message, line_separator='\r'):
    """Return a ParsedMessage object.

    Keyword arguments:
    line_separator -- the segment separator.  The segment
    separator is a hard coded part of the HL7 standard,
    but, in practice, being able to change it is beneficial.
    """

    parsed_message = ParsedMessage()

    # Field and Subcomponent separator locations
    # are a hard coded part of the HL7 standard
    field_separator = message[3]
    subcomponent_separator = message[4]

    for line in message.split(line_separator):
        repeated_segment = False

        fields = line.split(field_separator)
        segment_name = fields[0]

        if parsed_message.segment_exists(segment_name):
            segment = parsed_message.get_segment(segment_name)
            repeated_segment = True

        else:
            segment = HL7Segment()
            segment.name = segment_name

        subcomponents = []
        subcomponents.append([segment_name])
        field_start = 1
        if segment_name == 'MSH':
            subcomponents.append([field_separator])
            subcomponents.append([fields[1]])
            field_start = 2
        for field in fields[field_start:]:
            subcomponents.append(field.split(subcomponent_separator))
        segment.values.append(subcomponents)
        if not repeated_segment:
            parsed_message.segments.append(segment)

    return parsed_message
