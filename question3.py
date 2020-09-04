import json

def q3_calc(json_string):
    #get json tickets from parameter

    unique_dest_ip_by_hash = 0

    unique_dest_ip_by_hash_devided_by_sum_unique_hashes = 0.0

    #tickets
    tickets = json_string['tickets']

    # all hashes
    hashes_list = []


    # len of all tickets
    print( len(tickets) )


    # get all hashes in hashes_list
    for ticket in tickets:

        hashes_list.append( ticket['file_hash'] )

    # get unique hashes
    unique_hashes = set(hashes_list)

    #len of all unique hashes
    print( len( unique_hashes ) )

    #loop through all unique hashes
    #get relate dest ip adress
    #count uniqueness of ip adresses
    #get sum of uniqueness
    for hash in unique_hashes:

        list_dest = []

        # fill list_dest with related dest ip adresses
        for ticket in tickets:

            if ticket['file_hash'] == hash:
                list_dest.append( ticket['dst_ip'] )

        # get unique related dest ip adresses
        unique_dests = set(list_dest)

        #print the list
        print(list_dest)
        #print len of uniqueness
        print('count_uniqueness = {}'.format(len(unique_dests)))

        # get the sum
        unique_dest_ip_by_hash +=len(unique_dests)

    # get the total = len
    print('total = {}'.format(unique_dest_ip_by_hash))

    unique_dest_ip_by_hash_devided_by_sum_unique_hashes = unique_dest_ip_by_hash / len(unique_hashes)


    print('Resultas = {}'.format(unique_dest_ip_by_hash_devided_by_sum_unique_hashes))

    return unique_dest_ip_by_hash_devided_by_sum_unique_hashes
