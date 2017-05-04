def parse(message, line_separator='\r'):
    """Return a ParsedMessage object.

    Keyword arguments:
    line_separator -- the segment separator.  The segment
    separator is a hard coded part of the HL7 standard,
    but, in practice, being able to change it is beneficial.
    """

    parsed_message = ParsedMessage(message)

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


class ParsedMessage:
    """Parsed HL7 message object."""

    def __init__(self, message):
        self.segments = []
        self.raw_message = message
        self.raw_message_length = len(message)

    def get_segment(self, segment_name):
        """Return a HL7Segment object based on its name."""
        return [seg for seg in self.segments if seg.name == segment_name][0]

    def segment_exists(self, segment_name):
        """Return if a segment exists in the message based on its name."""
        return segment_name in [seg.name for seg in self.segments]

    def segment_count(self, segment_name=None):
        """Return the number of segments with a certain name or the count of all segments

        Keyword arguments:
        segment_name -- optional name of a segment. If provided, this function will
        return the number of segments of the same name.  Otherwise, this function
        will return the total number of segments
        """
        if segment_name is None:
            return sum(len(segment.values) for segment in self.segments)
        return len(self.get_segment(segment_name).values)

    def get_value(self, segment_name, repetition, field,
                  sub=1):
        """Return the value of a specific subcomponent

        segment_name is a string name of a segment, ex: 'MSH'.
        repetition is 0-based index of the segment repetition to return
        field is 0-based index of field on segement to return
        sub is 0-based index of subcomponent of field to return

        Keyword arguments:
        sub -- subcomponent index
        """

        # To enable 1-based indexing, we decrement the incoming arguments
        repetition -= 1
        sub -= 1

        segment = self.get_segment(segment_name)
        if (len(segment.values) > repetition and
                    len(segment.values[repetition]) > field and
                    len(segment.values[repetition][field]) > sub):
            return segment.values[repetition][field][sub]
        return None

class HL7Segment:
    """HL7 Segment object."""

    def __init__(self):
        self.values = []
        self.name = ''
