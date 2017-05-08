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

if parsed_message is None:
    raise Exception("Message did not parse.")

if parsed_message.raw_message != message:
    raise Exception("Raw message not properly saved.")

if parsed_message.raw_message_length != len(message):
    raise Exception("Raw message length not properly returned.")

# Segment Existence
segment_data = {'MSH' : 1, 'EVN': 1, 'PID': 1, 'NK1': 1, 'PV1': 1, 'GT1': 1, 'DG1': 1, 'IN1': 3, 'IN2': 2 }
for segment_name in segment_data:
    if not parsed_message.segment_exists(segment_name):
        raise Exception("{0} should exist, but doesn't!".format(segment_name))
    if segment_data[segment_name] != parsed_message.segment_count(segment_name):
        raise Exception("{0} segment count incorrect.".format(segment_name))


# Segment value testing

def segment_test(expected_values, segment_repetition=1):
    for field in range(0, len(parsed_message.get_segment(expected_values[0]).values[segment_repetition - 1])):
        current_value = parsed_message.get_value(expected_values[0], segment_repetition, field)
        if current_value != expected_values[field].split('^')[0] and not (field == 2 and expected_values[0] == 'MSH'):
            raise Exception('Value mismatch in {0}: {1} != {2}'.format(expected_values[0],
                                                                       current_value,
                                                                       expected_values[field].split('^')[0]))

msh_values = ['MSH', '|', '^~\&', 'AccMgr', '1', '', '', '20050110045504', '', 'ADT', '599102', 'P', '2.3', '', '', '']
evn_values = ['EVN', 'A01', '20050110045502', '', '', '', '', '']
pid_values = ['PID', '1', '', '10006579^^^1^MRN^1', '', 'DUCK^DONALD^D', '', '19241010', 'M', '', '1',
              '111 DUCK ST^^FOWL^CA^999990000^^M', '1', '8885551212', '8885551212', '1', '2', '',
              '40007716^^^AccMgr^VN^1', '123121234', '', '', '', '', '', '', '', '', '', '', 'NO']
nk1_values = ['NK1', '1', 'DUCK^HUEY', 'SO', '3583 DUCK RD^^FOWL^CA^999990000', '8885552222', '', 'Y', '', '', '', '',
              '', '', '', '', '', '', '', '', '', '']
pv1_values = ['PV1', '1', 'I', 'PREOP^101^1^1^^^S', '3', '', '', '37^DISNEY^WALT^^^^^^AccMgr^^^^CI', '', '', '01', '',
              '', '', '1', '', '', '37^DISNEY^WALT^^^^^^AccMgr^^^^CI', '2', '40007716^^^AccMgr^VN', '4', '', '', '', '',
              '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', 'G', '', '', '20050110045253', '', '',
              '', '', '', '']
gt1_values = ['GT1', '1', '8291', 'DUCK^DONALD^D', '', '111^DUCK ST^^FOWL^CA^999990000', '8885551212', '', '19241010',
              'M', '', '1', '123121234', '', '', '', '#Cartoon Ducks Inc', '111^DUCK ST^^FOWL^CA^999990000',
              '8885551212', '', 'PT', '']
dg1_values = ['DG1', '1', 'I9', '71596^OSTEOARTHROS NOS-L/LEG ^I9', 'OSTEOARTHROS NOS-L/LEG ', '', 'A', '']
in1_values = ['IN1', '1', 'MEDICARE', '3', 'MEDICARE', '', '', '', '', '', '', 'Cartoon Ducks Inc', '19891001', '', '',
              '4', 'DUCK^DONALD^D', '1', '19241010', '111^DUCK ST^^FOWL^CA^999990000', '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '', '123121234A', '', '', '', '', '', 'PT', 'M',
              '111 DUCK ST^^FOWL^CA^999990000', '', '', '', '', '8291']
in2_values = ['IN2', '1', '', '123121234', 'Cartoon Ducks Inc', '', '', '123121234A', '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '8885551212']
in1_2_values = ['IN1', '2', 'NON-PRIMARY', '9', 'MEDICAL MUTUAL CALIF.', 'PO BOX 94776^^HOLLYWOOD^CA^441414776', '',
                '8003621279', 'PUBSUMB', '', '', 'Cartoon Ducks Inc', '', '', '', '7', 'DUCK^DONALD^D', '1', '19241010',
                '111 DUCK ST^^FOWL^CA^999990000', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '056269770', '', '', '', '', '', 'PT', 'M', '111^DUCK ST^^FOWL^CA^999990000', '', '', '', '', '8291']
in2_2_values = ['IN2', '2', '', '123121234', 'Cartoon Ducks Inc', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '8885551212']
in1_3_values = ['IN1', '3', 'SELF PAY', '1', 'SELF PAY', '', '', '', '', '', '', '', '', '', '', '5', '', '1']
segment_test(msh_values)
segment_test(evn_values)
segment_test(pid_values)
segment_test(nk1_values)
segment_test(pv1_values)
segment_test(gt1_values)
segment_test(dg1_values)
segment_test(in1_values)
segment_test(in2_values)
segment_test(in1_2_values, 2)
segment_test(in2_2_values, 2)
segment_test(in1_3_values, 3)


exit(0)
