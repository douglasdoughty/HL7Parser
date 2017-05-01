class ParsedMessage:
    """Parsed HL7 message object."""

    def __init__(self):
        self.segments = []

    def get_segment(self, segment_name):
        """Return a HL7Segment object based on its name."""
        return [seg for seg in self.segments if seg.name == segment_name][0]


    def segment_exists(self, segment_name):
        """Return if a segment exists in the message based on its name."""
        return segment_name in [seg.name for seg in self.segments]


    def segment_count(self, segment_name):
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
