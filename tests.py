import HL7Parser

message = """MSH|^~\&|AccMgr|1|||20050110045504||ADT^A08|599102|P|2.3|||
EVN|A01|20050110045502|||||
PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111 DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO
NK1|1|DUCK^HUEY|SO|3583 DUCK RD^^FOWL^CA^999990000|8885552222||Y||||||||||||||
PV1|1|I|PREOP^101^1^1^^^S|3|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4|||||||||||||||||||1||G|||20050110045253||||||
GT1|1|8291|DUCK^DONALD^D||111^DUCK ST^^FOWL^CA^999990000|8885551212||19241010|M||1|123121234||||#Cartoon Ducks Inc|111^DUCK ST^^FOWL^CA^999990000|8885551212||PT|
DG1|1|I9|71596^OSTEOARTHROS NOS-L/LEG ^I9|OSTEOARTHROS NOS-L/LEG ||A|
IN1|1|MEDICARE|3|MEDICARE|||||||Cartoon Ducks Inc|19891001|||4|DUCK^DONALD^D|1|19241010|111^DUCK ST^^FOWL^CA^999990000|||||||||||||||||123121234A||||||PT|M|111 DUCK ST^^FOWL^CA^999990000|||||8291
IN2|1||123121234|Cartoon Ducks Inc|||123121234A|||||||||||||||||||||||||||||||||||||||||||||||||||||||||8885551212
IN1|2|NON-PRIMARY|9|MEDICAL MUTUAL CALIF.|PO BOX 94776^^HOLLYWOOD^CA^441414776||8003621279|PUBSUMB|||Cartoon Ducks Inc||||7|DUCK^DONALD^D|1|19241010|111 DUCK ST^^FOWL^CA^999990000|||||||||||||||||056269770||||||PT|M|111^DUCK ST^^FOWL^CA^999990000|||||8291
IN2|2||123121234|Cartoon Ducks Inc||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||8885551212
IN1|3|SELF PAY|1|SELF PAY|||||||||||5||1"""

parsed_message = HL7Parser.parse(message, '\n')

assert parsed_message is not None, "Message did not parse."
assert parsed_message.raw_message == message, "Raw message not properly saved."
assert parsed_message.raw_message_length == len(message), "Raw message length not properly returned."
assert parsed_message.segment_count() == 12, "Total segment count incorrect."
assert parsed_message.segment_count("MSH") == 1, "MSH segment count incorrect."
assert parsed_message.segment_count("EVN") == 1, "EVN segment count incorrect."
assert parsed_message.segment_count("PID") == 1, "PID segment count incorrect."
assert parsed_message.segment_count("NK1") == 1, "NK1 segment count incorrect."
assert parsed_message.segment_count("PV1") == 1, "PV1 segment count incorrect."
assert parsed_message.segment_count("GT1") == 1, "GT1 segment count incorrect."
assert parsed_message.segment_count("DG1") == 1, "DG1 segment count incorrect."
assert parsed_message.segment_count("IN1") == 3, "IN1 segment count incorrect."
assert parsed_message.segment_count("IN2") == 2, "IN2 segment count incorrect."


exit(0)
