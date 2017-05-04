[![Build Status](https://travis-ci.org/douglasdoughty/HL7Parser.svg?branch=master)](https://travis-ci.org/douglasdoughty/HL7Parser)

# HL7parser
Python based HL7 parser to easily pull information from an HL7 message.  The goal of this package is to allow quick access to
HL7 data stored within an HL7 message.  A great resource for explanations of the HL7 segments exists here: [http://hl7-definition.caristix.com:9010/](http://hl7-definition.caristix.com:9010/)

## Usage:
After importing HL7Parser, pass a string HL7 message to it's parse() function. If the message doesn't have HL7 default
line endings (carriage return), then pass the correct line separator as an optional second/named parameter. A
ParsedMessage object will be returned.  You can then use the get_value() function on this object to retrieve
specific values from the message.

```python
import HL7Parser

example_message = """MSH|^~\&|AccMgr|1|||20050110045504||ADT^A08|599102|P|2.3|||
EVN|A01|20050110045502|||||
PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111 DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO
NK1|1|DUCK^HUEY|SO|3583 DUCK RD^^FOWL^CA^999990000|8885552222||Y||||||||||||||
PV1|1|I|PREOP^101^1^1^^^S|3|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4|||||||||||||||||||1||G|||20050110045253||||||
GT1|1|8291|DUCK^DONALD^D||111^DUCK ST^^FOWL^CA^999990000|8885551212||19241010|M||1|123121234||||#Cartoon Ducks Inc|111^DUCK ST^^FOWL^CA^999990000|8885551212||PT|
DG1|1|I9|71596^OSTEOARTHROS NOS-L/LEG ^I9|OSTEOARTHROS NOS-L/LEG ||A|
IN1|1|MEDICARE|3|MEDICARE|||||||Cartoon Ducks Inc|19891001|||4|DUCK^DONALD^D|1|19241010|111^DUCK ST^^FOWL^CA^999990000|||||||||||||||||123121234A||||||PT|M|111 DUCK ST^^FOWL^CA^999990000|||||8291
IN2|1||123121234|Cartoon Ducks Inc|||123121234A|||||||||||||||||||||||||||||||||||||||||||||||||||||||||8885551212"
"""

# Parse the message
parsed_message = HL7Parser.parse(example_message, line_separator='\n')

# Pull out specific values based on position
patient_name = parsed_message.get_value('PID', 1, 5, 1)
```

## Functions
#### get_value(segment_name, repetition, field, sub=1)
The get_value() function on the ParsedMessage object takes 3 (optionally 4) parameters. The first parameter is the
string name of the specific segment to get.  The second parameter is which repetition of the segment to get. The third
parameter is the field to retrieve, and the (optional) fourth parameter is which sub component to retrieve. The
repetition, field, and sub are all 1-based indexed. The sub argument is optional because some fields do not have
sub-components.  Therefore, it may be omitted.

Examples:
```python
# Get the event recorded date/time from the EVN segment (no sub components)
event_recorded_date_time = parsed_message.get_value('EVN', 1, 2)

# Get the attending doctor's first name from the PV1 segment
attending_doctor = parsed_message.get_value('PV1', 1, 7, 3)

```

#### segment_count(segment_name=None)
The segment_count function on the ParsedMessage object takes 1 optional parameter: the string name of the segment.
It returns the number of repetitions of that segment which have been parsed.  If no segment_name is specified, then a
total count of all the segments is returned.

Example:
```python
if parsed_message.segment_count('PID') == 2:
    pid_1_date_of_birth = parsed_message.get_value('PID', 1, 7)
    pid_2_date_of_birth = parsed_message.get_value('PID', 2, 7)
   
total_segments = parsed_message.segment_count()

```

#### segment_exists(segment_name)
The segment_exists function on the ParsedMessage object takes 1 parameter: the string name of the segment.  If the
segment exists, a True is returned, otherwise False.

Example:
```python
if parsed_message.segment_exists('PID'):
    # Get pertinent PID segment information
```

## Properties

#### raw_message
The raw_message property on the ParsedMessage object returns the message before it was parsed.

#### raw_message_length
The raw_message_length property on the ParsedMessage object returns the length of the message before it was parsed.

---
## Extra
HL7Parser is tested against python versions 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, 3.5-dev, 3.6, 3.6-dev, 3.7-dev, &amp; nightly
on Linux and OSX using [Travis CI](https://travis-ci.org/). 