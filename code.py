import json

from pwn import *
from question3 import q3_calc
# --------------------NOTES
#
# add recieve lines function
#
# -------------------------

def recieve_lines(remote_connection, n):
    for i in range(n):
        print( b"Line: " + remote_connection.recvline() )


def question1(remote_connection, json_string):
    # "You'll need to consult the file `incidents.json` to answer the following questions.\n"
    # b'The first question is:
    # What is the most common source IP address?
    # If there is more than one IP address that is the most common,
    # you may give any of the most common ones.'
    question_1 = remote_connection.recvuntil("ones.").strip()
    print (b"The first question is: " + question_1 )
    source_ip_list = []

    for value in json_string["tickets"]:
           source_ip_list.append(value["src_ip"])

    most_common_source_ip = max(set(source_ip_list), key=source_ip_list.count)
    print ('most_common_source_ip\n')
    print (most_common_source_ip)
    print ('sending the most_common_source_ip\n')
    remote_connection.send(most_common_source_ip + "\n")
    print ('begin recieving\n')
    remote_connection.recv()

    result = remote_connection.recvline()
    print (b"Result: " + result )
    return result



def question2(remote_connection, json_string):
    # b'The second question is: \n\n
    # How many unique destination IP addresses were targeted by the source IP address 204.108.217.70?'
    # Unique destination ip adress :

    question_2 = remote_connection.recvuntil("?")

    print (b"The second question is: " + question_2)

    ip_address = re.findall(r'[0-9]+(?:\.[0-9]+){3}', question_2.decode('utf-8'))

    unique_destination_ip_addresses = []
    for value in json_string['tickets']:
        if (value['src_ip'] == ip_address.__getitem__(0)
        and value['dst_ip'] not in unique_destination_ip_addresses):
            unique_destination_ip_addresses.append(value['dst_ip'])

    print( "Unique destination ip adress :" )
    print (str(len(unique_destination_ip_addresses)))
    print( "Begin sending" )
    remote_connection.send(str(len(unique_destination_ip_addresses)) + "\n")
    print( "Begin recieving" )
    remote_connection.recv()

    result = remote_connection.recvline()
    print (b"Result: " + result )
    return result


def question3(remote_connection, json_string):
    # 'The third question is:
    # What is the number of unique destination ips a file is sent,
    # on average? Needs to be correct to 2 decimal places.'
    #19.04

    question_3 = remote_connection.recvuntil("places.")
    #
    print(b"The third question is: " + question_3)

    answer =  q3_calc(json_string)
    #answer = float( sum( sent_hash.values() ) ) / len( sent_hash )
    ##################"

    print("this is the researched answer")
    print(answer)
    #remote_connection.send(answer)

    remote_connection.send("{:.2f}".format(answer))
    remote_connection.send("\n")
    remote_connection.recv()
    result = remote_connection.recvline()
    print (b"Result: " + result )
    return result
    #
    # print ("{:.2f}".format(answer))
    # r.send("{:.2f}".format(answer) + "\n")
    # r.recv()
    # result = r.recvline()
    # print (b"Result: " + result)
    #
    # if result == "Correct!\n":
    #     print (r.recv())
    #     break
    # elif result == "Incorrect!\n":
    #     r.close()
    #     print ("\nAnswer is incorrect retrying after 2 sec ...\n")
    #     time.sleep(2)
    #     answer += 0.01
    #     continue


def main():
    with open('incidents.json', 'r') as f:
        json_string = json.load(f)

    answer = 0.00

    many_loop = 1
    start_loop = 0
    remote_connection = remote('2018shell1.picoctf.com', 10493)


    while start_loop < many_loop:



        print( remote_connection.recvuntil("questions.")  + b"\n" )

        result1 = question1(remote_connection, json_string)
        recieve_lines(remote_connection, 2)
        result2 = question2(remote_connection, json_string)
        recieve_lines(remote_connection, 2)
        result3 = question3(remote_connection, json_string)

        print('result3')
        print(result3)

        if result3 == b"Correct!\n":
            print("this is the flag :")
            print (remote_connection.recv())
            break
        else :
            pass


        start_loop+=1
    else:

        # if while loop end
        remote_connection.close()

        #

        #
        # # Question 3
        #
        # question_3 = r.recvuntil("places.")
        #
        # print(b"The third question is: " + question_3)
        #
        # print ("{:.2f}".format(answer))
        # r.send("{:.2f}".format(answer) + "\n")
        # r.recv()
        # result = r.recvline()
        # print (b"Result: " + result)
        #
        # if result == "Correct!\n":
        #     print (r.recv())
        #     break
        # elif result == "Incorrect!\n":
        #     r.close()
        #     print ("\nAnswer is incorrect retrying after 2 sec ...\n")
        #     time.sleep(2)
        #     answer += 0.01
        #     continue
if __name__ == '__main__':
    main()
